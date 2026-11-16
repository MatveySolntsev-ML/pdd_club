from django.conf import settings
from django.db import models

from questions.models import Question


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="favorites"
    )
    question = models.ForeignKey(
        Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="favorited_by"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=["user", "question"], name="unique_favorite"),
        ]

    def __str__(self):
        return f"{self.user} → {self.question}"


class ReviewList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="review_list"
    )
    question = models.ForeignKey(
        Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="in_review_lists"
    )

    class Meta:
        verbose_name = "Вопрос на повторение"
        verbose_name_plural = "Список на повторение"
        constraints = [
            models.UniqueConstraint(fields=["user", "question"], name="unique_review_item"),
        ]

    def __str__(self):
        return f"{self.user} → {self.question}"
