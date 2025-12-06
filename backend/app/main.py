from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.core.config import settings
from app.core.startup import startup_checks
from app.api.endpoints import auth, pages, users, documents, processing, cases, search, onboarding, analytics, notifications
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Knowledge Retention Platform for SMEs",
    version="0.1.0"
)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": str(exc.detail), "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error.get("loc", []))
        msg = error.get("msg", "Invalid value")
        errors.append(f"{field}: {msg}")
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Validation error", "details": errors}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "Internal server error"}
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression for responses > 500 bytes
app.add_middleware(GZipMiddleware, minimum_size=500)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Request logging middleware
class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        if duration > 2.0:
            logger.warning(f"Slow request: {request.method} {request.url.path} took {duration:.2f}s")
        return response

app.add_middleware(RequestLoggingMiddleware)

# Include routers
app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(users.router)
app.include_router(documents.router)
app.include_router(processing.router)
app.include_router(cases.router)
app.include_router(search.router)
app.include_router(onboarding.router)
app.include_router(analytics.router)
app.include_router(notifications.router)

# Startup event
@app.on_event("startup")
async def on_startup():
    startup_checks()

# Shutdown event
@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down Docent API...")
    # Close database connections
    from app.core.database import engine
    engine.dispose()
    logger.info("Database connections closed")

# Favicon
@app.get("/favicon.ico")
async def favicon():
    return {"message": "no favicon"}

# Health check endpoint
@app.get("/health")
async def health_check():
    from app.core.database import engine
    from sqlalchemy import text
    import os
    
    status = {"status": "healthy", "service": "docent", "checks": {}}
    
    # Database check
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status["checks"]["database"] = "ok"
    except Exception as e:
        status["checks"]["database"] = "error"
        status["status"] = "degraded"
    
    # Disk space check
    try:
        stat = os.statvfs("/")
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        status["checks"]["disk_free_gb"] = round(free_gb, 2)
        if free_gb < 1:
            status["status"] = "warning"
    except:
        status["checks"]["disk"] = "unknown"
    
    return status

logger.info(f"Docent API initialized - Environment: {settings.ENVIRONMENT}")
