from django.db.models import CASCADE, BooleanField, CharField, DateField, EmailField, ForeignKey, TextField, TimeField, PositiveIntegerField, SET_NULL, DateTimeField, OneToOneField


from apps.acess.models.user import User
from apps.common.models.base import BaseCreationModel
from apps.inventory.models.product import Product


class WishList(BaseCreationModel):
    """This is WishList model
    ********************************  Model Fields ********************************
    pk                  - id
    FK                  - user, product 
    """     
    
    user = ForeignKey(to=User, on_delete=CASCADE)  
    product = ForeignKey(to=Product, on_delete=CASCADE)
    
    class Meta (BaseCreationModel.Meta):
        default_related_name = "related_wish_list"
        
        
class Cart(BaseCreationModel):
    """This is Cart model
    ********************************  Model Fields ********************************
    pk                  - id
    FK                  - user  
    """
    
    user = OneToOneField(User, on_delete=CASCADE)
    
    class Meta (BaseCreationModel.Meta):
        default_related_name = "related_cart"
           
           
class CartItem(BaseCreationModel):
    """This is CartItem model
    ********************************  Model Fields ********************************
    pk                   - id
    FK                   - cart, product    
    PositiveIntegerField - quantity
    """   
    
    cart = ForeignKey(to=Cart, on_delete=CASCADE)
    product = ForeignKey(to=Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=1)
    
    class Meta (BaseCreationModel.Meta):
        default_related_name = "related_cart_items"        