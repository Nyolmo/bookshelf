from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from book.models import Book
from book.serializers import BookSerializer  # import nested serializer


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = (
            "username", "first_name", "last_name",
            "email", "bio", "password", "password2"
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = CustomUser(
            username=validated_data["username"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data["email"],
            bio=validated_data.get("bio", "")
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    # Nested favorites for read
    favorites = BookSerializer(many=True, read_only=True)
    # IDs for write
    favorite_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Book.objects.all(),
        source="favorites",
        write_only=True,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            "id", "username", "first_name", "last_name",
            "email", "bio", "favorites", "favorite_ids"
        )
        extra_kwargs = {
            "email": {"read_only": True}
        }