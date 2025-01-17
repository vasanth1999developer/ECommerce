from django.urls import path

from apps.acess.views.login_signup import (
    LoginApi,
    PasswordResetRequestView,
    PasswordResetView,
    ProfileRetrieveViewSet,
    SignupAPIViewViewSet,
    UserAddressRetrieveViewSet,
    UserProfileUpdateAPIViewSet,
)
from apps.acess.views.user import (
    UserAddressCUDApiViewSet,
    UserListViewSet,
    UserRetrieveViewSet,
    UserUpdateDeleteViewSet,
)
from apps.common.routers import AppSimpleRouter

API_URL_PREFIX = "v1/"

router = AppSimpleRouter()

# API Router for Signup.
router.register(f"{API_URL_PREFIX}signup", SignupAPIViewViewSet, basename="signup")
router.register(f"{API_URL_PREFIX}get-profile", ProfileRetrieveViewSet, basename="retrieve-user")
router.register(f"{API_URL_PREFIX}profile-update", UserProfileUpdateAPIViewSet, basename="update-profile")

# Address API
router.register(f"{API_URL_PREFIX}list-user-address", UserAddressRetrieveViewSet, basename="list-user-address")

# API Router for User
router.register(f"{API_URL_PREFIX}list-user", UserListViewSet, basename="list-profile")
router.register(f"{API_URL_PREFIX}get-user", UserRetrieveViewSet, basename="retrive-profile")
router.register(f"{API_URL_PREFIX}update&delete-user", UserUpdateDeleteViewSet, basename="delete-user")
router.register(f"{API_URL_PREFIX}user-Address", UserAddressCUDApiViewSet, basename="user-Address")


urlpatterns = [
    path(f"{API_URL_PREFIX}login/", LoginApi.as_view()),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/confirm/", PasswordResetView.as_view(), name="password-reset-confirm"),
] + router.urls
