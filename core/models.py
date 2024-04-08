from django.db import models

from .utils.db_utils import (
    CreateAndUpdateDateTimeModel,
    EncryptedTextAbstractModel,
    EncryptedTextModelQuerySet,
)


class YTDataV3CredentialsQuerySet(EncryptedTextModelQuerySet):
    def get_or_create(self, defaults=None, **kwargs):
        if text := kwargs.pop("api_key", None):
            kwargs["encrypted_text"] = text
        return super(YTDataV3CredentialsQuerySet, self).get_or_create(
            defaults=defaults, **kwargs
        )

    def get(self, *args, **kwargs):
        if text := kwargs.pop("api_key", None):
            kwargs["encrypted_text"] = text
        return super(YTDataV3CredentialsQuerySet, self).get(**kwargs)

    def filter(self, *args, **kwargs):
        if text := kwargs.pop("api_key", None):
            kwargs["encrypted_text"] = text
        return super(YTDataV3CredentialsQuerySet, self).filter(**kwargs)

    def create(self, *args, **kwargs):
        if text := kwargs.pop("api_key", None):
            kwargs["encrypted_text"] = text
        return super(YTDataV3CredentialsQuerySet, self).create(**kwargs)


class YTDataV3Credentials(EncryptedTextAbstractModel):
    project_id = models.CharField(primary_key=True)
    project_name = models.CharField()

    objects = YTDataV3CredentialsQuerySet.as_manager()

    @property
    def api_key(self):
        return self.encrypted_text

    @api_key.setter
    def api_key(self, value):
        self.encrypted_text = value

    @api_key.deleter
    def api_key(self):
        del self.encrypted_text

    class Meta:
        verbose_name = "YouTube Data V3 Credentials"
        verbose_name_plural = "YouTube Data V3 Credentials"

    def __str__(self):
        return f"<YTDataV3Credentials(project_id={self.project_id}, project_name={self.project_name})>"


class YTMetadata(CreateAndUpdateDateTimeModel):
    id = models.CharField(primary_key=True)
    title = models.CharField()
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    channel_name = models.CharField()

    class Meta:
        verbose_name = "YouTube MetaData"
        verbose_name_plural = "YouTube MetaDatas"

    def __str__(self):
        return f"<YTMetadata(channel_name={self.channel_name}, title={self.title})>"
