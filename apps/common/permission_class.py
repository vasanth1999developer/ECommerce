from rest_framework.permissions import BasePermission


class RoleBasedPermission(BasePermission):
    """
    Allows access only to users with a specific role.
    """

    allowed_roles = []

    def has_permission(self, request, view):
        user_role = getattr(request.user, "role", None)

        return user_role in self.allowed_roles
