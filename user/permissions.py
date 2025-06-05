from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message="Only owners can access endpoint"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'

class IsEmployee(BasePermission):
    message="Only employee can perform these operation."
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'