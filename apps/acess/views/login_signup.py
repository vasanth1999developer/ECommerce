import uuid
from datetime import timedelta

from django.core.mail import send_mail
from django.utils.timezone import now
from rest_framework import status
from rest_framework.authtoken.models import Token

from apps.acess.models import User
from apps.acess.models.user import Address, password_reset
from apps.acess.serializer.login_signup import (
    LoginSerializer,
    UserAddressesRetrive,
    UserCreateSerializer,
    UserRetrieveSerializer,
    UserUpdateSerializer,
)
from apps.common.views.api.base import AppAPIView, NonAuthenticatedAPIMixin
from apps.common.views.api.generic import (
    AppModelCreatePIViewSet,
    AppModelListAPIViewSet,
    AppModelRetrieveAPIViewSet,
    AppModelUpdateAPIViewSet,
)


class SignupAPIViewViewSet(NonAuthenticatedAPIMixin, AppModelCreatePIViewSet):
    """This SignUp API cretae and update the user in the application..."""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class LoginApi(NonAuthenticatedAPIMixin, AppAPIView):
    """LoginApiView API to authenticate a user..."""

    def post(self, request):
        """Handle the post method"""

        serializer = LoginSerializer(data=self.get_request().data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user_instance)
        return self.send_response(data=token.key)


class ProfileRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """Retrieve user details API..."""

    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserAddressRetrieveViewSet(AppModelListAPIViewSet):
    """Retrieve user details API..."""

    serializer_class = UserAddressesRetrive

    def get_queryset(self):
        """Override get_queryset()"""

        user = self.get_user()
        return Address.objects.filter(user=user)


class UserProfileUpdateAPIViewSet(AppModelUpdateAPIViewSet):
    """This API is used to update user profile..."""

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        """This method is used to get user profile"""

        return self.get_user()


class PasswordResetView(NonAuthenticatedAPIMixin, AppAPIView):
    """This is used reset password"""

    def post(self, request):
        """Handle the post method"""

        token = self.get_request().data.get("token")
        new_password = self.get_request().data.get("password")
        serializer = UserCreateSerializer()
        validated_password = serializer.validate_password(new_password)
        try:
            reset_entry = password_reset.objects.get(token=token, used=False)
        except password_reset.DoesNotExist:
            return self.send_error_response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_entry.expires_at < now():
            return self.send_error_response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)
        user = reset_entry.user
        user.set_password(validated_password)
        user.save()
        reset_entry.used = True
        reset_entry.save()
        return self.send_response({"message": "Password reset successful."}, status=status.HTTP_200_OK)


class PasswordResetRequestView(NonAuthenticatedAPIMixin, AppAPIView):
    """Password reset request view"""

    def post(self, request):
        """Handleing the post method"""

        email = self.get_request().data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return self.send_error_response(
                {"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND
            )
        token = str(uuid.uuid4())
        expires_at = now() + timedelta(hours=1)
        password_reset.objects.create(user=user, token=token, expires_at=expires_at)
        reset_url = f"https://127.0.0.1:8000/password-reset/confirm/{token}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_url}",
            from_email="noreply@yourdomain.com",
            recipient_list=[email],
        )
        return self.send_response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
