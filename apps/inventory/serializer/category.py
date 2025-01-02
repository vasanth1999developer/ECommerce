from apps.common.serializers import AppReadOnlyModelSerializer, AppWriteOnlyModelSerializer
from apps.inventory.models.category import Category, SubCategory


class CategorySerializer(AppWriteOnlyModelSerializer):
    """Category model serializer holds create, update & destroy."""
    
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = Category
        fields = ["name"]
        

class CategoryRetriveSerializer(AppReadOnlyModelSerializer):
    """Category model serializer holds retrive..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Category
        fields = ["id", "name",]        
        
        
class SubCategorySerializer(AppWriteOnlyModelSerializer):
    """SubCategory model serializer holds create, update & destroy.."""
    
    class Meta(AppWriteOnlyModelSerializer.Meta):
        model = SubCategory
        fields = ["name", "category"]
            
            
class SubCategoryRetriveSerializer(AppReadOnlyModelSerializer):
    """SubCategory model serializer holds retrive..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = SubCategory
        fields = ["id", "name", "category"]
        
        
