from apps.acess.choices import RoleTypeChoices
from apps.acess.models.user import Address, User
from apps.acess.serializer.login_signup import (
    UserListRetrieveSerializer,
    UserRetrieveSerializer,
    UserRoleUpdateSerializer,
)
from apps.acess.serializer.user import UserAddressSerializer
from apps.common.permission_class import RoleBasedPermission
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet, AppModelRetrieveAPIViewSet


class UserListViewSet(AppModelListAPIViewSet):
    """A UserListViewSet that provides `list` action..."""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = UserListRetrieveSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True)


class UserRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """A UserRetrieveViewSet that provides `retrieve` action..."""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.filter(is_deleted=False, is_active=True)


class UserUpdateDeleteViewSet(AppModelCUDAPIViewSet):
    """A UserDeleteViewSet that provides destroy and update action..."""

    permission_classes = [RoleBasedPermission]
    RoleBasedPermission.allowed_roles = [RoleTypeChoices.admin]
    serializer_class = UserRoleUpdateSerializer
    queryset = User.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        """Override the destroy(). To get the Instance of the task By filtering User and PK..."""

        pk = kwargs.get("pk")
        instance = User.objects.filter(pk=pk).first()
        if not instance:
            return self.send_error_response(data="User not found")
        self.perform_destroy(instance)
        return self.send_response(data="User Deleted task successfully..")

    def perform_destroy(self, instance):
        """Override the perform_destroy(). To do a Soft Delete by setting is_Delete=True..."""

        instance.is_deleted = True
        instance.save()


class UserAddressCUDApiViewSet(AppModelCUDAPIViewSet):
    """User Address create and update view set"""

    serializer_class = UserAddressSerializer
    queryset = Address.objects.all()

    def perform_create(self, serializer):
        """Set the `user` field to the currently logged-in user"""

        serializer.save(user=self.get_user())
