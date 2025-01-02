from apps.common.serializers import AppReadOnlyModelSerializer, AppWriteOnlyModelSerializer
from apps.inventory.models.salesorder import WishList
from apps.inventory.serializer.product import ProductReadSerializer


class WishlistCUDSerializer(AppWriteOnlyModelSerializer):
    """Wishlist model serializer holds create, update & destroy."""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = WishList
        fields = ["user", "product"]


class WishListRetriveSerializer(AppReadOnlyModelSerializer):
    """Wishlist model serializer holds read only fields."""

    product = ProductReadSerializer(read_only=True)

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = WishList
        fields = ["id", "user", "product"]
