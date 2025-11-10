from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().select_related("category").prefetch_related("authors")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    parser_classes = [MultiPartParser, FormParser]  # allow cover image upload

    # Filtering
    filterset_fields = ["category", "authors", "published_date"]

    # Search
    search_fields = ["title", "description", "isbn", "authors__name", "category__name"]

    # Ordering
    ordering_fields = ["title", "published_date", "created_at"]
    ordering = ["title"]

    lookup_field = "id"  # UUID lookups

    # Favorites toggle
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_favorite(self, request, id=None):
        book = self.get_object()
        user = request.user
        if book in user.favorites.all():
            user.favorites.remove(book)
            return Response({"status": "removed"})
        user.favorites.add(book)
        return Response({"status": "added"})


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "bio"]
    ordering_fields = ["name"]
    ordering = ["name"]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name"]
    ordering = ["name"]