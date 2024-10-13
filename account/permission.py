import logging
from ninja_extra.permissions import BasePermission
from ninja_extra import permissions
from django.contrib.auth.models import User
from ninja.errors import HttpError

# logger = logging.getLogger("account.permissions")
class UserWithPermission(permissions.BasePermission):
    def __init__(self, permission: str) -> None:
        self._permission = permission
        
    def has_permission(self, request, controller=None,view=None):
        user = request.user
        if not user.is_authenticated:
            raise HttpError(401, "Unauthorized")
        
        # Check if the user has the required permission directly
        if user.has_perm(self._permission):
            return True
        
        return any(user.has_perm(self._permission, group) for group in user.groups.all())
    
    # def has_permission(self, request,controller=None):
    #     return request.user.has_perm(self._permission)


