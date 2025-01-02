from rest_framework.exceptions import PermissionDenied

from apps.acess.choices import RoleTypeChoices
from apps.acess.models.user import Address, User
from apps.acess.serializer.login_signup import UserRetrieveSerializer, UserRoleUpdateSerializer
from apps.acess.serializer.user import UserAddressSerializer
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet, AppModelRetrieveAPIViewSet


class UserListViewSet(AppModelListAPIViewSet):
    """A UserListViewSet that provides `list` action..."""

    serializer_class = UserRetrieveSerializer

    def get_queryset(self):
        """Override get_queryset() method provided by GenericAPIView.
        For filtering the User based on is_deleted .
        """

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return User.objects.filter(is_deleted=False, is_active=True)
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class UserRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """A UserRetrieveViewSet that provides `retrieve` action..."""

    serializer_class = UserRetrieveSerializer

    def get_queryset(self):
        """Override get_queryset() method provided by GenericAPIView
        For filtering the User based on is_deleted...
        """

        user = self.request.user
        if user.role == RoleTypeChoices.admin:
            return User.objects.filter(is_deleted=False)
        else:
            raise PermissionDenied("You do not have permission to view this content.")


class UserUpdateDeleteViewSet(AppModelCUDAPIViewSet):
    """A UserDeleteViewSet that provides destroy and update action..."""

    serializer_class = UserRoleUpdateSerializer

    def get_queryset(self):
        """Override get_queryset() method provided by GenericAPIView.
        For filtering the task based on the logged in user and their task <pk>..."""

        queryset = User.objects.filter(is_deleted=False)
        return queryset

    def destroy(self, request, *args, **kwargs):
        """Override the destroy(). To get the Instance of the task By filtering User and PK..."""

        user = self.get_user()
        if user.role == RoleTypeChoices.admin:
            pk = kwargs.get("pk")
            instance = User.objects.filter(pk=pk).first()
            if not instance:
                return self.send_error_response(data="User not found")
            self.perform_destroy(instance)
            return self.send_response(data="User Deleted task successfully..")
        else:
            raise PermissionDenied("You do not have permission to view this content.")

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
        serializer.save(user=self.request.user)
