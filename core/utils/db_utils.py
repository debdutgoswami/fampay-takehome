import base64

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import models


class CreateAndUpdateDateTimeModel(models.Model):
    create_time = models.DateField(auto_now_add=True)
    update_time = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class EncryptedTextField(models.TextField):
    """Custom Encrypted Field"""

    salt = bytes(settings.SECURE_STRING_SALT, encoding="raw_unicode_escape")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend(),
    )

    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode("utf-8")))
    f = Fernet(key)

    @classmethod
    def encrypt(cls, value):
        return cls.f.encrypt(bytes(value, encoding="raw_unicode_escape")).decode(
            "utf-8"
        )

    @classmethod
    def decrypt(cls, value):
        return str(cls.f.decrypt(bytes(value, "utf-8")), encoding="raw_unicode_escape")

    @staticmethod
    def hash(value):
        return make_password(value, settings.SECURE_STRING_SALT)

    def from_db_value(self, value, expression, connection):
        return self.decrypt(value)

    def get_prep_value(self, value):
        return self.encrypt(value)


class EncryptedTextModelQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        if text := kwargs.pop("encrypted_text", None):
            kwargs["encrypted_hash"] = EncryptedTextField.hash(text)
        return super(EncryptedTextModelQuerySet, self).filter(*args, **kwargs)

    def get_or_create(self, defaults=None, **kwargs):
        if text := kwargs.pop("encrypted_text", None):
            kwargs["encrypted_hash"] = EncryptedTextField.hash(text)
            defaults["encrypted_text"] = text
        return super(EncryptedTextModelQuerySet, self).get_or_create(
            defaults=defaults, **kwargs
        )

    def get(self, *args, **kwargs):
        if text := kwargs.pop("encrypted_text", None):
            kwargs["encrypted_hash"] = EncryptedTextField.hash(text)
        return super(EncryptedTextModelQuerySet, self).get(*args, **kwargs)

    def create(self, *args, **kwargs):
        if text := kwargs.get("encrypted_text", None):
            kwargs["encrypted_hash"] = EncryptedTextField.hash(text)
        return super(EncryptedTextModelQuerySet, self).create(*args, **kwargs)


class EncryptedTextAbstractModel(CreateAndUpdateDateTimeModel):
    encrypted_text = EncryptedTextField()
    encrypted_hash = models.CharField(max_length=256, blank=True)

    objects = EncryptedTextModelQuerySet.as_manager()

    class Meta:
        abstract = True

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.encrypted_hash = EncryptedTextField.hash(self.encrypted_text)
        super(EncryptedTextAbstractModel, self).save(
            force_insert, force_update, using, update_fields
        )
