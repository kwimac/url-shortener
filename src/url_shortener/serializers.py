from typing import Any

from rest_framework import serializers

from .models import ShortURL


class URLSerializer(serializers.Serializer):
    class Meta:
        model = ShortURL
        fields = ["id", "created", "updated", "url", "url_hash"]

    id = serializers.UUIDField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    url = serializers.URLField(source="original_url")
    hash = serializers.CharField(read_only=True, max_length=10)

    def validate_url(self, url: str) -> str:
        if ShortURL.objects.filter(original_url=url).first():
            raise serializers.ValidationError("URL arleady in DB")
        return url

    def create(self, validated_data: dict[str, str]) -> Any:
        original_url = validated_data["original_url"]
        while True:
            uuid, url_hash = ShortURL.generate_hash(original_url)
            if ShortURL.objects.filter(hash=url_hash).first():
                continue
            return ShortURL.objects.create(
                id=uuid,
                original_url=original_url,
                hash=url_hash,
            )
