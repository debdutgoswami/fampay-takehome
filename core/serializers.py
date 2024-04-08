from rest_framework import serializers
from core.models import YTMetadata


class YTMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = YTMetadata
        fields = ["id", "title", "description", "published_at", "thumbnail_url"]
