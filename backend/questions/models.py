from django.conf import settings
from django.db import models

from core.models import TimestampedModel


class Topic(models.Model):
    """Тема раздела ПДД — аналог тега в проекте Фудграм."""

    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("Слаг", max_length=100, unique=True)

    class Meta:
        verbose_name = "Тема раздела ПДД"
        verbose_name_plural = "Темы разделов ПДД"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Question(TimestampedModel):
    STATUS_OPEN = "open"
    STATUS_RESOLVED = "resolved"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Опубликован"),
        (STATUS_RESOLVED, "Разъяснён"),
    ]

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE, related_name="questions"
    )
    topic = models.ForeignKey(Topic, verbose_name="Тема", on_delete=models.PROTECT, related_name="questions")
    ticket_number = models.PositiveSmallIntegerField("Номер билета")
    text = models.TextField("Текст вопроса")
    image = models.ImageField("Изображение", upload_to="questions/images/", blank=True, null=True)
    status = models.CharField("Статус", max_length=16, choices=STATUS_CHOICES, default=STATUS_OPEN)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Билет {self.ticket_number}: {self.text[:40]}"


class Comment(TimestampedModel):
    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст комментария")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author}: {self.text[:40]}"
