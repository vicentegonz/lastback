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
    date = models.DateField("date", default=date.today)
    category = models.CharField(max_length=255)
    net_sale = models.IntegerField()
    contribution = models.IntegerField()
    transactions = models.IntegerField()
    gross_sale = models.IntegerField()


class ServiceIndicator(BaseModel):
    store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name="services")
    date = models.DateField("date", default=date.today)
    amount_of_surveys = models.IntegerField()
    nps = models.IntegerField()
    amount_nps = models.IntegerField()
    experience = models.IntegerField()
    amount_experience = models.IntegerField()
    kindness = models.IntegerField()
    amount_kindness = models.IntegerField()
    waiting_time = models.IntegerField()
    amount_waiting_time = models.IntegerField()
    speed = models.IntegerField()
    amount_speed = models.IntegerField()
    quality = models.IntegerField()
    amount_quality = models.IntegerField()
    bathroom = models.IntegerField()
    amount_bathroom = models.IntegerField()


class Product(models.Model):
    description = models.CharField(max_length=255)
    stores = models.ManyToManyField(Store, related_name="products")
    supplier = models.CharField(max_length=255, null=True)
