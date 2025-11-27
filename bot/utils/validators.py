"""
Validation utilities.
"""
import re


def validate_phone(phone: str) -> bool:
    """Validate Kazakhstan phone number."""
    # Remove spaces, dashes, plus
    clean_phone = phone.replace(' ', '').replace('-', '').replace('+', '')
    # Should be 11 digits starting with 7
    return bool(re.match(r'^7\d{10}$', clean_phone))


def format_phone(phone: str) -> str:
    """Format phone to +7XXXXXXXXXX."""
    clean_phone = phone.replace(' ', '').replace('-', '').replace('+', '')
    if clean_phone.startswith('7'):
        return '+' + clean_phone
    elif clean_phone.startswith('8'):
        return '+7' + clean_phone[1:]
    else:
        return '+7' + clean_phone

