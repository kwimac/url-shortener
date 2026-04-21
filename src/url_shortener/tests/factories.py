import string
import uuid

import factory
import factory.fuzzy
from src.url_shortener.models import ShortURL


class ShortURLFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShortURL

    id = factory.LazyFunction(uuid.uuid4)
    created = factory.faker.Faker("date_time")
    modified = factory.faker.Faker("date_time")
    original_url = factory.faker.Faker("url")
    hash = factory.fuzzy.FuzzyText(length=10, chars=string.ascii_letters+string.digits)
