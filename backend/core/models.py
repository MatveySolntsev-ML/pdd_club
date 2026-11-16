from django.db import models


class TimestampedModel(models.Model):
    """Abstract base — reusable in any project, independent of the PDD domain."""
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        abstract = True
