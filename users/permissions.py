from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.authentication import MongoUser


def is_mongo_user(user):
    """Returns True only if the user is a real authenticated MongoUser."""
    return isinstance(user, MongoUser)


class IsAdmin(BasePermission):
    """Allow access only to Admin users."""
    message = 'Only Admins are allowed to perform this action.'

    def has_permission(self, request, view):
        return is_mongo_user(request.user) and request.user.role == 'Admin'


class IsAdminOrReadOnly(BasePermission):
    """
    Allow read access (GET, HEAD, OPTIONS) to any authenticated user.
    Allow write access (POST, PUT, PATCH, DELETE) only to Admins.
    """
    message = 'Only Admins are allowed to modify data.'

    def has_permission(self, request, view):
        if not is_mongo_user(request.user):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'Admin'

