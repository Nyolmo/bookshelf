import uuid
import random
from django.db import models
from django.utils.text import slugify


def generate_isbn13():
    """
    Generate a valid ISBN-13 number with check digit.
    """
    # Start with a 12-digit random number (prefix 978 or 979 is common for ISBNs)
    prefix = random.choice(["978", "979"])
    body = str(random.randint(10**9, (10**10) - 1))  # 10 random digits
    base = prefix + body  # 12 digits

    # Calculate check digit
    total = 0
    for i, digit in enumerate(base):
        n = int(digit)
        if i % 2 == 0:  # even index → weight 1
            total += n
        else:           # odd index → weight 3
            total += n * 3
    check_digit = (10 - (total % 10)) % 10

    return base + str(check_digit)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class Book(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name="books", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books"
    )
    published_date = models.DateField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to="book/covers/",
        blank=True,
        null=True
    )
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "Books"

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        # Auto-generate ISBN if missing
        if not self.isbn:
            self.isbn = generate_isbn13()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title