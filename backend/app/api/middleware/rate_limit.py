from collections import defaultdict
from fastapi import Request, HTTPException
import time

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str, max_requests: int = 10, window_seconds: int = 60) -> bool:
        """Check if request is allowed based on rate limit"""
        now = time.time()
        window_start = now - window_seconds
        
        # Clean old requests
        self.requests[key] = [t for t in self.requests[key] if t > window_start]
        
        # Check limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add request
        self.requests[key].append(now)
        return True
    
    def get_wait_time(self, key: str, window_seconds: int = 60) -> int:
        """Get seconds to wait before next request is allowed"""
        if not self.requests[key]:
            return 0
        oldest = min(self.requests[key])
        wait = int(oldest + window_seconds - time.time())
        return max(0, wait)

# Global rate limiter instance
rate_limiter = RateLimiter()

def check_rate_limit(request: Request, max_requests: int = 10, window_seconds: int = 60):
    """Dependency to check rate limit"""
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{request.url.path}"
    
    if not rate_limiter.is_allowed(key, max_requests, window_seconds):
        wait_time = rate_limiter.get_wait_time(key, window_seconds)
        raise HTTPException(
            status_code=429,
            detail=f"Too many requests. Please wait {wait_time} seconds."
        )
