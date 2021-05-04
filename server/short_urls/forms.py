from django.forms import ModelForm

from server.short_urls.models import ShortURL


class ShortURLForm(ModelForm):
    class Meta:
        model = ShortURL
        exclude = ["createdAt", "updatedAt"]
