from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from apps.acess.models import User
from apps.acess.serializer.login_signup import UserCreateSerializer, UserRetrieveSerializer, UserUpdateSerializer
from apps.common.views.api.base import AppAPIView, NonAuthenticatedAPIMixin
from apps.common.views.api.generic import AppModelCreatePIViewSet, AppModelRetrieveAPIViewSet, AppModelUpdateAPIViewSet


class SignupAPIViewViewSet(NonAuthenticatedAPIMixin, AppModelCreatePIViewSet):
    """This SignUp API cretae and update the user in the application..."""

    serializer_class = UserCreateSerializer


class LoginApi(NonAuthenticatedAPIMixin, AppAPIView):
    """LoginApiView API to authenticate a user..."""

    def post(self, request):
        """Handle the post method"""

        email = self.get_request().data["username"]
        password = self.get_request().data["password"]
        user_instance = User.objects.filter(email=email.lower()).first()
        if user_instance is None:
            return self.send_error_response(data="User Not found...Enter proper email address")
        if not user_instance.check_password(password):
            return self.send_error_response(data="Invalid password")
        token, created = Token.objects.get_or_create(user=user_instance)
        return self.send_response(data=token.key)


class ProfileRetrieveViewSet(AppModelRetrieveAPIViewSet):
    """Retrieve user details API..."""

    serializer_class = UserRetrieveSerializer

    def retrieve(self, request, *args, **kwargs):
        """override retrieve function to retrieve"""

        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class UserProfileUpdateAPIViewSet(AppModelUpdateAPIViewSet):
    """This API is used to update user profile..."""

    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def get_object(self):
        """This method is used to get user profile"""

        return self.request.user
