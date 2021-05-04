from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
        editable=False,
        null=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True, editable=False, null=True
    )

    class Meta:
        abstract = True
        ordering = ["created_at"]


class DecostructMixin:
    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # exclude all fields you dont want to cause migration
        for field in ("upload_to", "storage", "verbose_name", "help_text"):
            if field in kwargs:
                del kwargs[field]
        return name, path, args, kwargs


class ImageField(DecostructMixin, models.ImageField):
    pass


class FileField(DecostructMixin, models.FileField):
    pass
