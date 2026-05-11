"""Validation helpers for phone data and user input."""
import re

REQUIRED_PHONE_FIELDS = ("id", "brand", "model", "price")


def validate_phone_data(data: dict) -> bool:
    if not isinstance(data, dict):
        return False
    for f in REQUIRED_PHONE_FIELDS:
        if f not in data:
            return False
    return True


def validate_email(email: str) -> bool:
    """Simple email validator using regex."""
    if not isinstance(email, str) or not email:
        return False
    # Basic RFC-5322-ish pattern (simplified)
    pattern = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
