from rest_framework.decorators import action

from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet
from apps.meta.models.location import City, Country, State
from apps.meta.serializers.location import CityCUDModelSerializer, CountryCUDModelSerializer, StateCUDModelSerializer
from apps.common.serializers import get_app_read_only_serializer as read_serializer



class CountryCUDApiViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete countries"""

    serializer_class = CountryCUDModelSerializer
    queryset = Country.objects.all()


class CountryListApiViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve countries"""

    queryset = Country.objects.all()
    serializer_class = read_serializer(
        meta_model=Country,
        meta_fields=["id", "identity"],
    )
    search_fields = ["identity"]


class StateCUDApiViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete states"""

    serializer_class = StateCUDModelSerializer
    queryset = State.objects.all()


class StateListApiViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve states"""

    queryset = State.objects.all()
    serializer_class = read_serializer(
        meta_model=State,
        meta_fields=["id", "identity", "country"],
    )
    search_fields = ["identity"]
    filterset_fields = ["country"]

    @action(detail=False)
    def meta(self, request, *args, **kwargs):
        """Filter Meta for Frontend."""

        country = self.serializer_class().serialize_for_meta(
            Country.objects.all(), fields=["id", "identity"]
        )
        data = {"country": country}
        return self.send_response(data)


class CityCUDApiViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete cities"""

    serializer_class = CityCUDModelSerializer
    queryset = City.objects.all()


class CityListApiViewSet(AppModelListAPIViewSet):
    """Api viewset to retrieve cities"""

    queryset = City.objects.all()
    serializer_class = read_serializer(
        meta_model=City,
        meta_fields=["id", "identity", "state"],
    )
    search_fields = ["identity"]
    filterset_fields = ["state"]

    @action(detail=False)
    def meta(self, request, *args, **kwargs):
        """Filter Meta for Frontend."""

        state = self.serializer_class().serialize_for_meta(
            State.objects.all(), fields=["id", "identity"]
        )
        data = {"state": state}
        return self.send_response(data)
