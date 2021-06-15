from datetime import date

from django.db import models

from backend.accounts.models import User
from backend.common.models import BaseModel


class Zone(BaseModel):
    name = models.CharField(max_length=255)


class Store(BaseModel):
    users = models.ManyToManyField(User, related_name="stores")
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT, related_name="stores")
    address = models.CharField(max_length=255)

    def notify_users(self, body, data=None):
        for user in self.users.all():
            user.devices.all().send_push_notification(body, data)


class Event(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="events")
    data = models.JSONField()

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.store.notify_users(body="New event created!")
        super().save(*args, **kwargs)


class KPI(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="KPIs")
    name = models.CharField(max_length=255)
    value = models.FloatField()
    units = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255)
    date = models.DateField("date", default=date.today)


class ServiceIndicator(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="services")
    name = models.CharField(max_length=255)
    value = models.FloatField()
    amount_of_surveys = models.IntegerField()
    date = models.DateField("date", default=date.today)


class Product(models.Model):
    description = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="products")
