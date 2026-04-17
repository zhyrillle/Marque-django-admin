from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from bson import ObjectId
from .auth_utils import decode_token
from .db import get_users_collection
import jwt


class MongoUser:
    """
    A lightweight user object built from a MongoDB document.
    Mimics enough of Django's user interface for DRF to work.
    """
    def __init__(self, doc):
        self.id = str(doc['_id'])
        self.username = doc.get('username')
        self.role = doc.get('role')
        self.firstname = doc.get('firstname', '')
        self.lastname = doc.get('lastname', '')
        self.email = doc.get('email', '')
        self.is_authenticated = True
        self.is_active = True

    def __str__(self):
        return self.username


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            payload = decode_token(token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        users = get_users_collection()
        try:
            doc = users.find_one({'_id': ObjectId(payload['user_id'])})
        except Exception:
            raise AuthenticationFailed('Invalid user ID in token.')

        if not doc:
            raise AuthenticationFailed('User not found.')

        return (MongoUser(doc), token)
