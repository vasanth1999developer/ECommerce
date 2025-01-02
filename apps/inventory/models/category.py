
from django.db.models import CharField, ForeignKey, CASCADE
from apps.common.models.base import COMMON_CHAR_FIELD_MAX_LENGTH, BaseCreationModel, SoftDeleteModel


class  Category(BaseCreationModel):
    """
    User model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    charField           - name
    """
     
    name = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)
        
    class Meta (BaseCreationModel.Meta):
        default_related_name = "related_categories"
         

class SubCategory(BaseCreationModel):     
    """
    User model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    charField           - name
    fk                  - category
    """
    
    name = CharField(max_length=COMMON_CHAR_FIELD_MAX_LENGTH, unique=True)
    category = ForeignKey(to=Category, on_delete=CASCADE)

    class Meta (BaseCreationModel.Meta):
        default_related_name = "related_SubCategories"
        
        
 