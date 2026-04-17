import jwt
from datetime import datetime, timedelta
from django.conf import settings


def generate_token(user_id, role):
    payload = {
        'user_id': str(user_id),
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_token(token):
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
