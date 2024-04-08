from django.contrib import admin

from core.models import YTDataV3Credentials, YTMetadata


@admin.register(YTDataV3Credentials)
class YTDataV3CredentialsAdmin(admin.ModelAdmin):
    pass


@admin.register(YTMetadata)
class YTMetadataAdmin(admin.ModelAdmin):
    list_display = ("title", "channel_name")
    search_fields = ("id", "title", "channel_name")
    ordering = ("-published_at",)
