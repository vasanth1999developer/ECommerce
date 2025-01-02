from apps.common.routers import AppSimpleRouter
from apps.meta.views import (
    CityCUDApiViewSet,
    CityListApiViewSet,
    CountryCUDApiViewSet,
    CountryListApiViewSet,
    StateCUDApiViewSet,
    StateListApiViewSet,
)

API_URL_PREFIX = "api/v1/meta"

app_name = "meta"

router = AppSimpleRouter()

# Country Api's
router.register(f"{API_URL_PREFIX}/country/cud", CountryCUDApiViewSet)
router.register(f"{API_URL_PREFIX}/country/list", CountryListApiViewSet, basename="country-list")

# State Api's
router.register(f"{API_URL_PREFIX}/state/cud", StateCUDApiViewSet)
router.register(f"{API_URL_PREFIX}/state/list", StateListApiViewSet, basename="state-list")

# City Api's
router.register(f"{API_URL_PREFIX}/city/cud", CityCUDApiViewSet)
router.register(f"{API_URL_PREFIX}/city/list", CityListApiViewSet, basename="city-list")



urlpatterns = [] + router.urls
