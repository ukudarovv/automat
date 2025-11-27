"""
Telegram Web App authentication utilities.
"""
import hashlib
import hmac
from urllib.parse import parse_qsl
from django.conf import settings
from bot.config import TELEGRAM_BOT_TOKEN


def validate_telegram_init_data(init_data: str) -> dict:
    """
    Validate Telegram Web App initData.
    
    Args:
        init_data: Raw initData string from Telegram Web App
        
    Returns:
        dict: Parsed and validated user data, or None if invalid
    """
    try:
        # Parse init_data
        parsed_data = dict(parse_qsl(init_data))
        
        # Extract hash
        received_hash = parsed_data.pop('hash', '')
        if not received_hash:
            return None
        
        # Create data check string
        data_check_string = '\n'.join(
            f"{key}={value}" 
            for key, value in sorted(parsed_data.items())
        )
        
        # Calculate secret key
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=TELEGRAM_BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()
        
        # Verify hash
        if calculated_hash != received_hash:
            return None
        
        # Parse user data
        user_data = {}
        if 'user' in parsed_data:
            import json
            user_data = json.loads(parsed_data['user'])
        
        return {
            'user': user_data,
            'auth_date': parsed_data.get('auth_date'),
            'query_id': parsed_data.get('query_id'),
        }
    except Exception as e:
        return None


def get_user_from_init_data(init_data: str):
    """
    Get or create user from Telegram initData.
    
    Returns:
        User object or None
    """
    from core.models import User
    
    validated_data = validate_telegram_init_data(init_data)
    if not validated_data or 'user' not in validated_data:
        return None
    
    user_data = validated_data['user']
    telegram_id = user_data.get('id')
    
    if not telegram_id:
        return None
    
    # Get or create user
    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            'username': f"user_{telegram_id}",
            'first_name': user_data.get('first_name', ''),
            'last_name': user_data.get('last_name', ''),
            'role': 'student'
        }
    )
    
    # Update user info if exists
    if not created:
        if user_data.get('first_name'):
            user.first_name = user_data['first_name']
        if user_data.get('last_name'):
            user.last_name = user_data['last_name']
        if user_data.get('username'):
            user.username = user_data['username']
        user.save()
    
    return user

