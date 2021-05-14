from django.db import models

from backend.accounts.models import User


class Zone(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)


class Store(models.Model):
    users = models.ManyToManyField(User, related_name="stores")
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="stores")
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)


class Event(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="events")
    data = models.JSONField()
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)
