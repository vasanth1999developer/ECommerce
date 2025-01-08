from django.db.models import CASCADE, CharField, ForeignKey

from apps.common.models.base import COMMON_CHAR_FIELD_MAX_LENGTH, BaseCreationModel


class Category(BaseCreationModel):
    """
    User model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    charField           - name
    Unique              - uuid
    Datetime            - created_at, modified_at
    Fk                  - created_by
    """

    name = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_categories"


class SubCategory(BaseCreationModel):
    """
    User model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    charField           - name
    fk                  - category, created_by
    Unique              - uuid
    Datetime            - created_at, modified_at
    """

    name = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)
    category = ForeignKey(to=Category, on_delete=CASCADE)

    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_sub_categories"
