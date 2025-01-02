from rest_framework import serializers

from apps.common.serializers import AppReadOnlyModelSerializer, AppWriteOnlyModelSerializer
from apps.inventory.models.product import Image, Offer, Product, ProductSpecification, Specification


class ProductWriteSerializer(AppWriteOnlyModelSerializer):
    """Product model serializer holds create, update & destroy..."""
    
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Product
        fields = ["name", "description", "price", "final_price", "available_stock", "discount", "sub_category"]
        extra_kwargs = {
            "final_price": {"read_only": True},
        }
        
    def create(self, validated_data):
        """Override create to calculate final_price before saving..."""
        
        price = validated_data.get("price")
        discount = validated_data.get("discount", 0)
        validated_data["final_price"] = price * (1 - discount / 100) if price and discount else price
        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        """Override update to calculate final_price before saving..."""
        
        price = validated_data.get("price", instance.price)
        discount = validated_data.get("discount", instance.discount)
        instance.final_price = price * (1 - discount / 100) if price and discount else price
        return super().update(instance, validated_data)     
 
 
class ProducImageSerializer(AppWriteOnlyModelSerializer):
    """Product Image model serializer holds create, update & destroy..."""
      
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Image
        fields = ["product", "image"]
         
        
class ImageReadSerializer(AppReadOnlyModelSerializer):
    """Product Image model serializer holds read only fields..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Image
        fields = ["id", "image", "product"]
    

class ProductOfferReadSerializer(AppReadOnlyModelSerializer):
    """Product Offer model serializer holds read only fields..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Offer
        fields = ["id", "type", "offer_description", "product"]            
            
  
class SpecificationRetriveSerializer(AppReadOnlyModelSerializer):
    """Specification model serializer holds create, update & destroy..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Specification
        fields = ["id","key", "sub_category"]   
        
        
class SpecificationkeyretriveSerializer(AppReadOnlyModelSerializer):
    """Specification model serializer to retrive key..."""    
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Specification
        fields = ("__all__")
        
                  
class ProductSpecificationNameSerializer(AppReadOnlyModelSerializer):
    """Product Specification model serializer..."""
    
    related_Specification = SpecificationkeyretriveSerializer(many=True, read_only=True)
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = ProductSpecification 
        fields = ("related_Specification", "value" )  
                     
                    
class ProductReadSerializer(AppReadOnlyModelSerializer):
    """Product model serializer holds read only fields..."""
    
    related_images = ImageReadSerializer(many=True, read_only=True)
    related_offers = ProductOfferReadSerializer(many=True, read_only=True)
    related_product_specifications = ProductSpecificationNameSerializer(many=True, read_only=True,)
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Product
        fields = ["id", "name", "description", "price", "final_price", "available_stock", "discount", "sub_category", "related_images", "related_offers", "related_product_specifications"]
            

class productOfferWriteSerializer(AppWriteOnlyModelSerializer):
    """Product Offer model serializer holds create, update & destroy..."""
     
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Offer
        fields = ["type", "offer_description", "product"]
            
            
class SpecificationSerializer(AppWriteOnlyModelSerializer):
    """Specification model serializer holds create, update & destroy..."""
    
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Specification
        fields = ["key", "sub_category"]            
            
    
class ProductSpecificationSerializer(AppWriteOnlyModelSerializer):
    """Product Specification model serializer..."""
    
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = ProductSpecification 
        fields = ("product", "specification", "value" ) 