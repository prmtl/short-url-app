import string

from django.db import models
from django.utils.translation import gettext_lazy as _

from hashid_field import HashidAutoField

from server.core.models import TimeStampedModel


class ShortURL(TimeStampedModel):
    _HASHID_SALT = "ShortURL"  # for simplicity
    _HASHID_ALPHABET = string.ascii_lowercase + string.digits

    id = HashidAutoField(
        verbose_name=_("ID"),
        primary_key=True,
        salt=_HASHID_SALT,
        alphabet=_HASHID_ALPHABET,
    )
    # NOTE(prmtl): max_length is set to a more or less valid
    # value coming from https://stackoverflow.com/a/417184/1490344
    # that (according to the materials there) should be enough for
    # now and can be always adjusted
    original = models.URLField(
        verbose_name=_("original"), max_length=2000, unique=True
    )

    def __str__(self):
        return f"{self.original[:32]} (id: {self.id})"
