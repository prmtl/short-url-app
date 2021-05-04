from django.forms import ModelForm
from django.utils.translation import gettext as _

from server.short_urls.models import ShortURL


class ShortURLForm(ModelForm):
    class Meta:
        model = ShortURL
        exclude = ["createdAt", "updatedAt"]
