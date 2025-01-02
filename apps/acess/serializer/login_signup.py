from rest_framework import serializers

from apps.acess.models.user import Address, User
from apps.common.serializers import AppCreateModelSerializer, AppReadOnlyModelSerializer


def validate_first_name(value):
    """Validate username. it Should not contain any special characters and should not contain numbers..."""

    if not value or not value.strip():
        raise serializers.ValidationError("Username cannot be empty or null.")
    if any(char in '!@#$%^&*()_+{}:"<>?/.,;[]=-1234567890' for char in value):
        raise serializers.ValidationError("Username cannot contain special characters and numbers.")
    return value.lower()
 
def validate_last_name(value):
    """Validate username. it Should not contain any special characters and should not contain numbers..."""

    if not value or not value.strip():
        raise serializers.ValidationError("Username cannot be empty or null.")
    if any(char in '!@#$%^&*()_+{}:"<>?/.,;[]=-1234567890' for char in value):
        raise serializers.ValidationError("Username cannot contain special characters and numbers.")
    return value.lower() 


class UserCreateSerializer(AppCreateModelSerializer):
    """This is CUD Serializer for User model..."""
    
    gender = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(validators=[validate_last_name])

    first_name = serializers.CharField(validators=[validate_first_name])
    class Meta(AppCreateModelSerializer.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "password", "phone_number", "gender", "role")

    def validate_password(self, password):
        """
        Validate the password....
        By  length of password
        And presence of at least one uppercase letter,
        One lowercase letter,
        One digit and
        One special character.
        """

        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in password):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%&*()+=_-;:?/><[]{},." for char in password):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return password
    
    def validate_email(self, value):
        """Convert the Email into a Lowercase..."""

        return value.lower()
    
    def create(self, validated_data):
        """By this method password hashing is implemented..."""
              
        password = validated_data.pop("password")
        first_name = validated_data.pop("first_name", None)
        last_name = validated_data.pop("last_name", None)
        phone_number = validated_data.pop("phone_number", None)
        gender = validated_data.pop("gender", None)        
        user = User.objects.create_user(password=password, **validated_data)
        if first_name and last_name and phone_number and gender:  
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.gender = gender
            user.save()
        return user
    
    
class UserAddressesRetrive(AppReadOnlyModelSerializer):
    """This serializer is used to retrieve User's addresses..."""
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Address
        fields =("__all__")     
            
    
class UserRetrieveSerializer(AppReadOnlyModelSerializer):
    """This is RetrieveSerializer for User model..."""
    
    related_addresses = UserAddressesRetrive(many=True, read_only=True)
    
    class Meta(AppReadOnlyModelSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "gender", "role", "related_addresses")   
        
        
class UserUpdateSerializer(AppCreateModelSerializer):
    """This is update Serializer for User model..."""
    
    gender = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(validators=[validate_last_name])
    first_name = serializers.CharField(validators=[validate_first_name])
    class Meta(AppCreateModelSerializer.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "gender" )
    
    
    def validate_email(self, value):
        """Convert the Email into a Lowercase..."""

        return value.lower()
    
    def update(self, instance, validated_data):
        """ This update method is ovverrided to update the instance"""      
               
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance    
    
    
class UserRoleUpdateSerializer(AppCreateModelSerializer):
    """This is RoleUpdate Serializer for User model..."""   
        
    class Meta(AppCreateModelSerializer.Meta):
        model = User
        fields = ("role",)
        
    def update(self, instance, validated_data):
        """Override the update method to update the User's role."""

        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance    