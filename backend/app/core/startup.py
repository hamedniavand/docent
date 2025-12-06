import os
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

def validate_environment():
    """Validate required environment variables on startup"""
    required = [
        'DATABASE_URL',
        'JWT_SECRET',
        'GEMINI_API_KEY',
    ]
    
    missing = []
    for var in required:
        if not getattr(settings, var, None):
            missing.append(var)
    
    if missing:
        logger.warning(f"Missing environment variables: {', '.join(missing)}")
    else:
        logger.info("✅ All required environment variables set")
    
    # Check database connection
    try:
        from sqlalchemy import text
        from app.core.database import engine
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection verified")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
    
    # Check storage paths
    storage_path = getattr(settings, 'STORAGE_PATH', '/data/storage')
    if os.path.exists(storage_path):
        logger.info(f"✅ Storage path exists: {storage_path}")
    else:
        try:
            os.makedirs(storage_path, exist_ok=True)
            logger.info(f"✅ Storage path created: {storage_path}")
        except Exception as e:
            logger.error(f"❌ Cannot create storage path: {e}")

def startup_checks():
    """Run all startup checks"""
    logger.info("Running startup checks...")
    validate_environment()
    logger.info("Startup checks complete")
