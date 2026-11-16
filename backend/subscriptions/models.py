from django.conf import settings
from django.db import models


class Subscription(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Подписчик", on_delete=models.CASCADE, related_name="subscriptions"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Автор", on_delete=models.CASCADE, related_name="subscribers"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=["follower", "author"], name="unique_subscription"),
            models.CheckConstraint(check=~models.Q(follower=models.F("author")), name="prevent_self_subscription"),
        ]

    def __str__(self):
        return f"{self.follower} → {self.author}"
