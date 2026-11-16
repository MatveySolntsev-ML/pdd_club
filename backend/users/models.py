from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_USER = "user"
    ROLE_MODERATOR = "moderator"
    ROLE_CHOICES = [
        (ROLE_USER, "Пользователь"),
        (ROLE_MODERATOR, "Модератор"),
    ]

    email = models.EmailField("Email", unique=True)
    role = models.CharField("Роль", max_length=16, choices=ROLE_CHOICES, default=ROLE_USER)
    avatar = models.ImageField("Аватар", upload_to="users/avatars/", blank=True, null=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR
