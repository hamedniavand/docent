import re
import html
from typing import Optional

def sanitize_html(text: str) -> str:
    """Escape HTML to prevent XSS"""
    if not text:
        return ""
    return html.escape(text)

def sanitize_filename(filename: str) -> str:
    """Remove dangerous characters from filename"""
    if not filename:
        return "unnamed"
    # Remove path separators and null bytes
    filename = filename.replace("/", "_").replace("\\", "_").replace("\x00", "")
    # Remove other dangerous characters
    filename = re.sub(r'[<>:"|?*]', '_', filename)
    # Limit length
    if len(filename) > 200:
        ext = filename.rsplit('.', 1)[-1] if '.' in filename else ''
        filename = filename[:190] + ('.' + ext if ext else '')
    return filename

def validate_email(email: str) -> bool:
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Check password meets minimum requirements"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is strong"

def sanitize_search_query(query: str) -> str:
    """Sanitize search query"""
    if not query:
        return ""
    # Remove special characters that could be dangerous
    query = re.sub(r'[<>"\';\\]', '', query)
    # Limit length
    return query[:500].strip()
