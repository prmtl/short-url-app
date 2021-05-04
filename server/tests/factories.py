import factory


class ShortURLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "short_urls.ShortURL"

    original = factory.Faker("url")
