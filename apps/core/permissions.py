from rest_framework.permissions import BasePermission


class IsTenantUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'institution') and request.user.institution_id is not None


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        required = getattr(view, 'required_roles', [])
        if not required:
            return True
        return request.user.is_authenticated and request.user.role in required


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ('super_admin', 'institution_admin')
