from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE, BooleanField, CharField, DateField, EmailField, ForeignKey, TextField, TimeField, PositiveIntegerField, SET_NULL, DateTimeField

from apps.acess.choices import GenderChoices, RoleTypeChoices, TagTypeChoices
from apps.common import models
from apps.common.managers import UserManager
from apps.common.model_fields import AppPhoneNumberField
from apps.common.models.base import (
    COMMON_CHAR_FIELD_MAX_LENGTH,
    COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    BaseArchivableModel,
    BaseCreationModel,
    BaseModel, 
)
from apps.common.validations import validate_pincode


class User(AbstractUser, BaseArchivableModel):
    """
    User model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    charField           - password, role, first_name, last_name, role
    DateTimeField       - created_at,modified_at
    EmailField          - email
    PhoneNumberField    - phone_number
    """
    
    username = None
    phone_number = AppPhoneNumberField(**COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG)   
    first_name = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    last_name = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )    
    gender = CharField(
        choices=GenderChoices.choices,
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
    )     
    email = EmailField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        unique=True
    )
    role = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        choices=RoleTypeChoices.choices,
        default=RoleTypeChoices.member,
    )    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()


    class Meta(BaseCreationModel.Meta):
        default_related_name = "related_users"

     
class Address(BaseModel):
    """
    Address model for the application...

    ********************************  Model Fields ********************************
    pk                     - id
    charField              - tag, address, city, country, state
    DateTimeField          - created_at,modified_at
    PositiveIntegerField   - pincode
    FK                     - user
    """       
       
    tag = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH, 
        choices=TagTypeChoices.choices,
    )
    address = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    city = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    country = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    state = CharField(
        max_length=COMMON_CHAR_FIELD_MAX_LENGTH,
        **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG,
    )
    pincode = PositiveIntegerField(
        validators=[validate_pincode], **COMMON_BLANK_AND_NULLABLE_FIELD_CONFIG
    )
    user = ForeignKey(to=User, on_delete=CASCADE)
           
    
    class Meta(BaseModel.Meta):
        default_related_name = "related_addresses"
       
    def __str__(self):
        return self.address         
 
 
class password_reset(BaseModel):
    """
    Password reset model for the application...

    ********************************  Model Fields ********************************
    pk                  - id
    CharField           - token
    DateTimeField       - expires_at, created_at
    BooleanField        - used
    ForeignKey          - user
    """
    
    token = CharField(max_length=255, unique=True)
    expires_at = DateTimeField()
    created_at = DateTimeField(auto_now_add=True)
    used = BooleanField(default=False)
    user = ForeignKey(User, on_delete=CASCADE, related_name="password_resets")
    
    
    class Meta(BaseModel.Meta):
               default_related_name = "related_password_resets"    

    def __str__(self):
        return f"Password Reset for {self.user.email} - Used: {self.used}"