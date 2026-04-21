from typing import Any

from django.db import IntegrityError
from rest_framework import serializers

from .models import ShortURLModel
from .utils import standardize_url


class URLSerializer(serializers.Serializer):
    class Meta:
        model = ShortURLModel
        fields = ["id", "created", "updated", "url", "url_hash"]

    id = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    url = serializers.URLField(source="original_url")
    hash = serializers.CharField(read_only=True, max_length=10)

    def validate_url(self, url: str) -> str:
        url = standardize_url(url)
        if not url:
            raise serializers.ValidationError("Given value is not a valid URL")
        if ShortURLModel.objects.filter(original_url=url).first():
            raise serializers.ValidationError("URL arleady in DB")
        return url

    def create(self, validated_data: dict[str, str]) -> Any:
        original_url = validated_data["original_url"]
        while True:
            uuid, url_hash = ShortURLModel.generate_hash(original_url)
            try:
                return ShortURLModel.objects.create(
                    id=uuid,
                    original_url=original_url,
                    hash=url_hash,
                )
            except IntegrityError:
                pass
