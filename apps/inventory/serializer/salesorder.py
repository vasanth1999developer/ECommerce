from apps.common.serializers import AppReadOnlyModelSerializer, AppWriteOnlyModelSerializer
from apps.inventory.models.salesorder import Cart, CartItem, Invoice, Order, Payment, WishList
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


class CartItemSerializer(AppReadOnlyModelSerializer):
    """CartItem model serializer holds read only fields."""

    product = ProductReadSerializer(read_only=True)

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = CartItem
        fields = ["id", "product", "quantity", "price", "discount", "final_price"]


class CartSerializer(AppReadOnlyModelSerializer):
    """Cart model serializer holds read only fields."""

    related_cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Cart
        fields = [
            "id",
            "user",
            "related_cart_items",
        ]

    def to_representation(self, instance):
        """Overriden the to_representation"""

        representation = super().to_representation(instance)
        total_price = sum(item.final_price for item in instance.related_cart_items.all())
        representation["total_price"] = total_price
        total_discount = sum(
            (item.price * item.quantity) - item.final_price for item in instance.related_cart_items.all()
        )
        representation["total_discount"] = total_discount
        if total_price > 5000:
            representation["delivery_charges"] = 0
        else:
            representation["delivery_charges"] = 50
        return representation


class OrderSerializer(AppWriteOnlyModelSerializer):
    """OrderSerializer class holds write only fields"""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Order
        fields = ["id", "user", "cart", "total_price", "total_discount", "delivery_charges", "payment_status"]


class PaymentSerializer(AppWriteOnlyModelSerializer):
    """Payment serializer class write only fields"""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Payment
        fields = ["id", "order", "payment_id", "status", "amount", "created_at"]


class InvoiceSerializer(AppWriteOnlyModelSerializer):
    """Invoice serializer for write-only fields"""

    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Invoice
        fields = ["id", "order", "pdf_path", "created_at"]
