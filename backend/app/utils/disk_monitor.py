import shutil
import logging

logger = logging.getLogger(__name__)

def check_disk_space(path: str = "/", min_gb: float = 1.0) -> dict:
    """
    Check available disk space
    Returns: dict with total, used, free (in GB) and warning
    """
    try:
        stat = shutil.disk_usage(path)
        total_gb = stat.total / (1024**3)
        used_gb = stat.used / (1024**3)
        free_gb = stat.free / (1024**3)
        percent_used = (used_gb / total_gb) * 100
        
        warning = free_gb < min_gb
        
        return {
            "total_gb": round(total_gb, 2),
            "used_gb": round(used_gb, 2),
            "free_gb": round(free_gb, 2),
            "percent_used": round(percent_used, 1),
            "warning": warning,
            "message": f"Low disk space: {free_gb:.1f}GB free" if warning else "Disk space OK"
        }
    except Exception as e:
        logger.error(f"Error checking disk space: {e}")
        return {"error": str(e)}