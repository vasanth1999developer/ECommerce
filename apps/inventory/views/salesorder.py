import razorpay
from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404
from razorpay.errors import BadRequestError
from rest_framework import status

from apps.acess.models.user import Address
from apps.common.views.api.base import AppAPIView
from apps.common.views.api.generic import AppModelCUDAPIViewSet, AppModelListAPIViewSet
from apps.inventory.models.product import Product
from apps.inventory.models.salesorder import Cart, CartItem, Order, WishList
from apps.inventory.serializer.salesorder import (
    CartSerializer,
    OrderSerializer,
    WishlistCUDSerializer,
    WishListRetriveSerializer,
)


class AddProductWishListCUDViewSet(AppModelCUDAPIViewSet):
    """Api viewset to create, update & delete product wishlist"""

    serializer_class = WishlistCUDSerializer

    def create(self, request, *args, **kwargs):
        """Create a wishlist entry for a product."""

        user = self.get_user()
        product_id = kwargs.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return self.send_error_response(data={"Product not found"})
        if WishList.objects.filter(user=user, product=product).exists():
            return self.send_error_response(data={"alredy added to your wishlist"})
        WishList.objects.create(user=user, product=product)
        return self.send_response(data={"added to your wishlist"})

    def destroy(self, request, *args, **kwargs):
        """Remove a specific product from the wishlist."""

        user = self.get_user()
        product_id = kwargs.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return self.send_error_response(data={"Product not found"})
        wishlist_entry = WishList.objects.filter(user=user, product=product).first()
        if not wishlist_entry:
            return self.send_error_response(data={"Product not found in your wishlist"})
        wishlist_entry.delete()
        return self.send_response(data={"Product removed from your wishlist"})


class UserWishListRetrieveViewSet(AppModelListAPIViewSet):
    """A UserWishListRetrieveViewSet that provides `retrieve` action..."""

    serializer_class = WishListRetriveSerializer

    def get_queryset(self):
        """Override get_queryset()"""

        user = self.get_user()
        return WishList.objects.filter(user=user)


class MoveWishListToCartView(AppAPIView):
    """API view to move items from the wishlist to the shopping cart."""

    def post(self, request):
        """Create function to convert product in wishlist to cart"""

        user = self.get_user()
        product_id = request.data.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        wishlist_item = get_object_or_404(WishList, user=user, product=product)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.final_price += product.final_price
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=1,
                discount=product.discount,
                price=product.price,
                final_price=product.final_price,
            )
        wishlist_item.delete()
        return self.send_response(data={"Product moved from your wishlist to shoppingcart"})


class CartRetriveForUserViewSet(AppModelListAPIViewSet):
    """This Api to retrive cart based on logged in user"""

    serializer_class = CartSerializer

    def get_queryset(self):
        """Override get_queryset()"""

        user = self.get_user()
        return Cart.objects.filter(user=user)


class OrderCUDApiViewSet(AppModelCUDAPIViewSet):
    """API viewset to create, update & delete orders"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create method for Order"""

        final_price = request.data.get("total_price")
        total_discount = request.data.get("total_discount")
        delivery_charges = request.data.get("delivery_charges")
        shipping_address = request.data.get("shipping_address")
        user = self.get_user()
        cart = Cart.objects.get(user=user, is_active=True)
        address = Address.objects.get(id=shipping_address)
        if final_price <= 0:
            return self.send_response({"error": "Invalid final price"}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(
            user=user,
            cart=cart,
            total_price=final_price,
            total_discount=total_discount,
            shipping_address=address,
            delivery_charges=delivery_charges,
            payment_status="PENDING",
        )
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        try:
            razorpay_order = client.order.create(
                {
                    "amount": int(final_price * 100),
                    "currency": "INR",
                    "receipt": f"order_rcptid_{order.id}",
                    "notes": {
                        "order_id": order.id,
                        "user_id": user.id,
                    },
                }
            )
        except BadRequestError as e:
            return self.send_response(
                {"error": f"Razorpay Order creation failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST
            )
        order.razorpay_order_id = razorpay_order["id"]
        order.save()
        user_phone_number = str(user.phone_number)
        payment_link = client.payment_link.create(
            {
                "amount": int(final_price * 100),
                "currency": "INR",
                "accept_partial": False,
                "description": "Order Payment",
                "customer": {
                    "email": user.email,
                    "contact": user_phone_number,
                },
                "notify": {
                    "sms": True,
                    "email": True,
                },
                "reminder_enable": True,
                "notes": {
                    "order_id": order.id,
                    "user_id": user.id,
                },
            }
        )
        payment_link_url = payment_link["short_url"]
        print(f"Payment link generated: {payment_link_url}")
        return self.send_response(
            {
                "message": "Payment link generated successfully",
                "payment_link": payment_link_url,
                "order_id": order.id,
            },
            status=status.HTTP_201_CREATED,
        )
