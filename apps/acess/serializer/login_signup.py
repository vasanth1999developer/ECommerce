from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from apps.acess.models.user import Address, User
from apps.common.serializers import AppCreateModelSerializer, AppReadOnlyModelSerializer, AppUpdateModelSerializer


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
        fields = ("first_name", "last_name", "email", "password", "phone_number", "gender")

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
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserAddressesRetrive(AppReadOnlyModelSerializer):
    """This serializer is used to retrieve User's addresses..."""

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = Address
        fields = ("id", "tag", "address", "city", "country", "state", "pincode", "user")


class UserRetrieveSerializer(AppReadOnlyModelSerializer):
    """This is RetrieveSerializer for User model..."""

    related_addresses = UserAddressesRetrive(many=True, read_only=True)

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "gender", "related_addresses", "role")


class UserListRetrieveSerializer(AppReadOnlyModelSerializer):
    """This is ListRetrieveSerializer for User model..."""

    class Meta(AppReadOnlyModelSerializer.Meta):
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "gender", "role")


class UserUpdateSerializer(AppUpdateModelSerializer):
    """This is update Serializer for User model..."""

    gender = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(validators=[validate_last_name])
    first_name = serializers.CharField(validators=[validate_first_name])

    class Meta(AppUpdateModelSerializer.Meta):
        model = User
        fields = ("first_name", "last_name", "email", "phone_number", "gender")

    def validate_email(self, value):
        """Convert the Email into a Lowercase..."""

        return value.lower()


class UserRoleUpdateSerializer(AppUpdateModelSerializer):
    """This is RoleUpdate Serializer for User model..."""

    class Meta(AppUpdateModelSerializer.Meta):
        model = User
        fields = ("role",)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_email(self, value):
        """Validate the email format and existence."""

        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format...")
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist...")
        return value

    def validate(self, data):
        """Custom validation for email and password combination."""

        email = data.get("email")
        password = data.get("password")
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError({"email": "User does not exist"})
        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Invalid password"})
        data["user"] = user
        return data
