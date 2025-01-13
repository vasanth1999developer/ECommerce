from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    IntegerField,
    OneToOneField,
    PositiveIntegerField,
    TextField,
)

from apps.acess.choices import PaymentStatusChoice, RatingChoice
from apps.acess.models.user import Address, User
from apps.common.models.base import COMMON_CHAR_FIELD_MAX_LENGTH, BaseCreationModel
from apps.inventory.models.product import Product


class WishList(BaseCreationModel):
    """This is WishList model
    ********************************  Model Fields ********************************
    pk                  - id
    FK                  - user, product, created_by
    Unique              - uuid
    Datetime            - created_at, modified_at
    """

    user = ForeignKey(to=User, on_delete=CASCADE)
    product = ForeignKey(to=Product, on_delete=CASCADE)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_wish_list"


class Cart(BaseCreationModel):
    """This is Cart model
    ********************************  Model Fields ********************************
    pk                  - id
    FK                  - user, created_by
    BooleanField        - is_active
    Unique              - uuid
    Datetime            - created_at, modified_at
    """

    user = OneToOneField(to=User, on_delete=CASCADE)
    is_active = BooleanField(default=True)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_cart"


class CartItem(BaseCreationModel):
    """This is CartItem model
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - cart, product, created_by
    PositiveIntegerField - quantity
    DecimalField         - price, discount
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    cart = ForeignKey(to=Cart, on_delete=CASCADE)
    product = ForeignKey(to=Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)
    price = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_price = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_cart_items"


class Order(BaseCreationModel):
    """This is CartItem model
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - user, cart, product, billing_address, shipping_address, created_by
    PositiveIntegerField - quantity
    DecimalField         - delivery_charges, total_discount, final_price, total_price
    DateField            - created_at, updated_at
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    user = ForeignKey(to=User, on_delete=CASCADE)
    cart = ForeignKey(to=Cart, on_delete=CASCADE)
    total_price = DecimalField(max_digits=10, decimal_places=2)
    shipping_address = ForeignKey(to=Address, on_delete=CASCADE)
    total_discount = DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_charges = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    payment_status = CharField(max_length=50, choices=PaymentStatusChoice.choices, default=PaymentStatusChoice.pending)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_orders"


class OrderItem(BaseCreationModel):
    """This is OrderItem model
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - order, product, created_by,
    PositiveIntegerField - quantity
    Unique               - uuid
    Datetime             - created_at, modified_at
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    user = ForeignKey(to=User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_order_items"


class RatingReview(BaseCreationModel):
    """This is RatingReview model
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - cart, product, order, created_by
    IntegerField         - rating
    TextField            - review
    DateField            - created_at
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    user = ForeignKey(to=User, on_delete=CASCADE)
    product = ForeignKey(Product, on_delete=CASCADE)
    rating = IntegerField(choices=RatingChoice.choices)
    review = TextField(blank=True, null=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_rating_reviews"


class Payment(BaseCreationModel):
    """Payment Model to track payment details.
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - order, created_by
    CharField            - payment_id, status,
    DecimalField         - amount
    DateField            - created_at
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    order = OneToOneField(Order, on_delete=CASCADE)
    payment_id = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)
    status = CharField(max_length=50, choices=[("SUCCESS", "Success"), ("FAILED", "Failed")])
    amount = DecimalField(max_digits=10, decimal_places=2)
    created_at = DateTimeField(auto_now_add=True)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_payments"


class Invoice(BaseCreationModel):
    """Invoice Model to store generated invoices.
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - order, created_by
    CharField            - pdf_path
    DateField            - created_at
    Unique               - uuid
    Datetime             - created_at, modified_at
    """

    order = OneToOneField(Order, on_delete=CASCADE)
    pdf_path = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    created_at = DateTimeField(auto_now_add=True)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_invoices"
