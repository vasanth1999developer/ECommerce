from apps.common.serializers import AppWriteOnlyModelSerializer
from apps.meta.models import City, Country, State


class CountryCUDModelSerializer(AppWriteOnlyModelSerializer):
    """Country model serializer holds create, update & destroy."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Country
        fields = ["identity"]


class StateCUDModelSerializer(AppWriteOnlyModelSerializer):
    """State model serializer holds create, update & destroy."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = State
        fields = ["identity", "country"]

    def get_meta(self) -> dict:
        """Get meta & the  initial values."""

        return {"country": self.serialize_for_meta(Country.objects.all(), fields=["id", "identity"])}


class CityCUDModelSerializer(AppWriteOnlyModelSerializer):
    """City model serializer holds create, update & destroy."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = City
        fields = ["identity", "state"]

    def get_meta(self) -> dict:
        """Get meta & the  initial values."""

        return {"state": self.serialize_for_meta(State.objects.all(), fields=["id", "identity"])}
