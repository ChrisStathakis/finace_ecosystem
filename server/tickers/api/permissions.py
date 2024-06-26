from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated


class IsAuthenticatedCustom(permissions.BasePermission):
    message = "You have to login to see this endpoint"

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(detail=self.message)
        return True