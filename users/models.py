from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from book.models import Book


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    favorites = models.ManyToManyField(Book, related_name="favorited_by", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username