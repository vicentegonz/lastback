from datetime import date

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

    def notify_users(self, body, data=None):
        for user in self.users.all():
            user.devices.all().send_push_notification(body, data)


class Event(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="events")
    data = models.JSONField()
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.store.notify_users(body="New event created!")
        super().save(*args, **kwargs)


class KPI(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="KPIs")
    name = models.CharField(max_length=255)
    value = models.FloatField()
    category = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    date = models.DateField("date", default=date.today)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)


class ServiceIndicator(models.Model):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="services")
    name = models.CharField(max_length=255)
    value = models.FloatField()
    amount_of_surveys = models.IntegerField()
    date = models.DateField("date", default=date.today)
    created_at = models.DateTimeField("created_at", auto_now_add=True)
    updated_at = models.DateTimeField("updated_at", auto_now=True)


class Product(models.Model):
    description = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="products")
