from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password, check_password
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from .auth_utils import generate_token
from .db import get_users_collection


def serialize_user(doc):
    """Convert a MongoDB document to a JSON-safe dict (without password)."""
    return {
        'id': str(doc['_id']),
        'username': doc.get('username'),
        'firstname': doc.get('firstname'),
        'middlename': doc.get('middlename', ''),
        'lastname': doc.get('lastname'),
        'email': doc.get('email', ''),
        'contact_number': doc.get('contact_number', ''),
        'role': doc.get('role'),
        'profile_image': doc.get('profile_image', ''),
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        users = get_users_collection()

        required = ['username', 'password', 'firstname', 'lastname', 'role']
        for field in required:
            if not data.get(field):
                return Response(
                    {'error': f'{field} is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if users.find_one({'username': data['username']}):
            return Response(
                {'error': 'Username already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if data.get('email') and users.find_one({'email': data['email']}):
            return Response(
                {'error': 'Email already exists.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if data['role'] not in ['Admin', 'Student']:
            return Response(
                {'error': 'Role must be Admin or Student.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_doc = {
            'username': data['username'],
            'password': make_password(data['password']),
            'firstname': data['firstname'],
            'lastname': data['lastname'],
            'role': data['role'],
            'profile_image': data.get('profile_image', ''),
        }

        # Only include optional fields if they have a value
        if data.get('middlename'):
            user_doc['middlename'] = data['middlename']
        if data.get('email'):
            user_doc['email'] = data['email']
        if data.get('contact_number'):
            user_doc['contact_number'] = data['contact_number']


        try:
            result = users.insert_one(user_doc)
        except DuplicateKeyError as e:
            # Figure out which field caused the conflict
            err_str = str(e)
            if 'email' in err_str:
                msg = 'Email already exists.'
            elif 'username' in err_str:
                msg = 'Username already exists.'
            else:
                msg = 'A user with this information already exists.'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)

        user_doc['_id'] = result.inserted_id
        token = generate_token(str(result.inserted_id), user_doc['role'])
        return Response(
            {'token': token, 'user': serialize_user(user_doc)},
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = get_users_collection()
        user = users.find_one({'username': username})

        if not user or not check_password(password, user['password']):
            return Response(
                {'error': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token = generate_token(str(user['_id']), user['role'])
        return Response({'token': token, 'user': serialize_user(user)})


class MeView(APIView):
    """Returns the currently logged-in user's info."""

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'email': user.email,
            'role': user.role,
        })
