from apps.acess.models.user import Address
from apps.common.serializers import AppCreateModelSerializer


class UserAddressSerializer(AppCreateModelSerializer):
    """This is CUD Serializer for UserAddress model..."""

    class Meta(AppCreateModelSerializer.Meta):
        model = Address
        fields = ["id", "tag", "address", "city", "state", "country", "pincode"]

    def update(self, instance, validated_data):
        """Update an existing Address instance with validated data."""

        instance.tag = validated_data.get("tag", instance.tag)
        instance.address = validated_data.get("address", instance.address)
        instance.city = validated_data.get("city", instance.city)
        instance.state = validated_data.get("state", instance.state)
        instance.country = validated_data.get("country", instance.country)
        instance.pincode = validated_data.get("pincode", instance.pincode)
        instance.save()
        return instance
