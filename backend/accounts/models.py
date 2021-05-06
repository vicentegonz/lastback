# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


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
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    picture = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contacts = models.ManyToManyField(self)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def generate_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
