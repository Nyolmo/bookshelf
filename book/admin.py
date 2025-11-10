from django.contrib import admin
from .models import Category, Author, Book


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "description")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "bio")
    search_fields = ("name", "bio")
    ordering = ("name",)


class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "published_date",
        "isbn",
        "slug",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "description", "isbn")
    list_filter = ("category", "published_date")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [AuthorInline]
    ordering = ("title",)
    autocomplete_fields = ("category", "authors")
    readonly_fields = ("created_at", "updated_at")