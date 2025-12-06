from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import auth, pages, users, documents, processing
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException, cases, search, onboarding, analytics, notifications

import logging

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

# Security headers middleware
from starlette.middleware.base import BaseHTTPMiddleware

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
import time

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Log slow requests (>2 seconds)
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
app.include_router(analytics.router)
app.include_router(notifications.router)
app.include_router(search.router)
app.include_router(onboarding.router)


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "docent"}

# Root endpoint
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Knowledge Retention Platform</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }
            .container {
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 { color: #2c3e50; }
            .status { color: #27ae60; font-weight: bold; }
            .info { margin: 20px 0; line-height: 1.6; }
            .endpoint { 
                background: #ecf0f1;
                padding: 10px;
                border-radius: 4px;
                margin: 10px 0;
                font-family: monospace;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 20px;
                font-weight: 600;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Docent</h1>
            <p class="status">✓ System Online</p>
            <div class="info">
                <p><strong>Knowledge Retention Platform</strong></p>
                <p>Version: 0.1.0 (MVP Development)</p>
                <p>Environment: Production</p>
            </div>
            <h3>Available Endpoints:</h3>
            <div class="endpoint">GET /health - Health check</div>
            <div class="endpoint">GET /docs - API documentation</div>
            <div class="endpoint">GET /auth/login-page - Login page</div>
            <div class="endpoint">POST /auth/login - Login API</div>
            <div class="endpoint">GET /auth/me - Current user info</div>
            <div class="endpoint">GET /dashboard - User dashboard</div>
            
            <a href="/auth/login-page" class="btn">Go to Login →</a>
            
            <p style="margin-top: 30px; color: #7f8c8d; font-size: 14px;">
                Day 4: Authentication system complete ✓
            </p>
        </div>
    </body>
    </html>
    """

logger.info(f"Docent API initialized - Environment: {settings.ENVIRONMENT}")