from apps.acess.models.user import Address
from apps.common.serializers import AppWriteOnlyModelSerializer


class UserAddressSerializer(AppWriteOnlyModelSerializer):
    """This is CUD Serializer for UserAddress model..."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Address
        fields = ["id", "tag", "address", "city", "state", "country", "pincode"]
