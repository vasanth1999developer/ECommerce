from django.db.models import CASCADE, BooleanField, CharField, DecimalField, ForeignKey, IntegerField, TextField

from apps.acess.choices import OfferChoice
from apps.common.models.base import COMMON_CHAR_FIELD_MAX_LENGTH, AppImageModel, BaseCreationModel, SoftDeleteModel
from apps.inventory.models.category import SubCategory


class Product(BaseCreationModel, SoftDeleteModel):
    """
    Product model for the application...
    ********************************  Model Fields ********************************
    pk                  - id
    charField           - name,
    TextField           - description
    DecimalField        - price, final_price, discount
    BooleanField        - is_stock_available
    IntegerField        - available_stock
    FK                  - sub_category
    """

    name = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    description = TextField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    price = DecimalField(max_digits=10, decimal_places=2)
    final_price = DecimalField(max_digits=10, decimal_places=2)
    is_stock_available = BooleanField(default=True)
    sub_category = ForeignKey(to=SubCategory, on_delete=CASCADE)
    available_stock = IntegerField()
    discount = DecimalField(max_digits=10, decimal_places=2)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_products"


class Specification(BaseCreationModel):
    """
    Specification model for the application...
    ********************************  Model Fields ********************************
    pk                  - id
    charField           - key
    FK                  - sub_category
    """

    sub_category = ForeignKey(to=SubCategory, on_delete=CASCADE)
    key = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_Specification"


class ProductSpecification(BaseCreationModel):
    """
    ProductSpecification model for the application...
    ********************************  Model Fields ********************************
    pk                  - id
    charField           - value
    FK                  - product, specification
    """

    product = ForeignKey(Product, on_delete=CASCADE)
    specification = ForeignKey(Specification, on_delete=CASCADE)
    value = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_product_specifications"


class Image(BaseCreationModel, AppImageModel):
    """
    Image model for the application...
    ********************************  Model Fields ********************************
    pk                  - id
    ImageField          - image
    FK                  - product
    """

    product = ForeignKey(to=Product, on_delete=CASCADE)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_images"


class Offer(BaseCreationModel):
    """Offers model for the application...
    ********************************  Model Fields ********************************
    pk                  - id
    CharField           - type
    FK                  - product
    TextField           - offer_description
    """

    type = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        choices=OfferChoice.choices,
        default=OfferChoice.no_offers,
    )
    offer_description = TextField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH)
    product = ForeignKey(to=Product, on_delete=CASCADE)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_offers"
