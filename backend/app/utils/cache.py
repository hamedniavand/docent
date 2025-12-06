from functools import wraps
from datetime import datetime, timedelta
from typing import Any, Optional
import hashlib
import json

class SimpleCache:
    """Simple in-memory cache with TTL"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key in self._cache:
            value, expires_at = self._cache[key]
            if datetime.utcnow() < expires_at:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value with TTL (default 5 minutes)"""
        expires_at = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expires_at)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear all cache"""
        self._cache = {}
    
    def cleanup(self):
        """Remove expired entries"""
        now = datetime.utcnow()
        expired = [k for k, (v, exp) in self._cache.items() if now >= exp]
        for k in expired:
            del self._cache[k]

# Global cache instance
cache = SimpleCache()

def cached(ttl_seconds: int = 300):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_data = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # Call function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl_seconds)
            return result
        return wrapper
    return decorator
