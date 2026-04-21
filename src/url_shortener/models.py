import hashlib
import uuid

from django.db import models

from model_utils.models import TimeStampedModel, UUIDModel


class ShortURLModel(TimeStampedModel, UUIDModel):
    original_url = models.URLField(null=False, unique=True, max_length=256)
    hash = models.CharField(null=False, unique=True, max_length=8)

    @staticmethod
    def generate_hash(url: str) -> tuple[uuid.UUID, str]:
        uuid_ = uuid.uuid4()
        url_hash = hashlib.sha1(f"{url}_{uuid_}".encode("UTF-8")).hexdigest()[:10]
        return uuid_, url_hash
