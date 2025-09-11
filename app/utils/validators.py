import re

def validate_email(email: str) -> bool:
    """Check if email looks valid"""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
