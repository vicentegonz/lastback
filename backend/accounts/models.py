from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from backend.common.queries import ExtendedQ

from .push_notifications import Notificator


class UserManager(BaseUserManager):
    def create_user(self, email, given_name, family_name, picture):
        if email is None:
            raise TypeError("Users should have a Email")

        user = self.model(
            email=self.normalize_email(email),
            given_name=given_name,
            family_name=family_name,
            picture=picture,
        )
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (0, "Manager"),
        (1, "Zone leader"),
    )

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=ROLE_CHOICES, default=0, max_length=100)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class DeviceQuerySet(models.QuerySet):
    def send_push_notification(self, body, data=None):
        notificator = Notificator()

        for device in self:
            notificator.send(device=device, body=body, data=data)


class DeviceManager(models.Manager):
    def get_queryset(self):
        return DeviceQuerySet(self.model, using=self._db)


class Device(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=ExtendedQ(android_id__isnull=False)
                ^ ExtendedQ(ios_id__isnull=False),
                name="exactly_one_os_id",
            )
        ]

    user = models.ForeignKey(
        User, null=True, related_name="devices", on_delete=models.SET_NULL
    )

    android_id = models.CharField(unique=True, null=True, max_length=255)
    ios_id = models.CharField(unique=True, null=True, max_length=255)

    expo_push_token = models.CharField(unique=True, null=True, max_length=255)

    objects = DeviceManager()

    @property
    def os(self):
        return (self.android_id and "Android") or (self.ios_id and "iOS")

    @property
    def os_id(self):
        return self.android_id or self.ios_id

    def __str__(self):
        return f"{self.user or 'Some one'}’s {self.os}"
