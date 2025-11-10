# book/serializers.py
from rest_framework import serializers
from .models import Category, Author, Book


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "description", "slug")


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name", "bio")


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        source="authors",
        write_only=True
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "description",
            "authors",
            "author_ids",
            "category",
            "category_id",
            "published_date",
            "isbn",
            "cover_image",
            "slug",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("slug", "created_at", "updated_at")