from rest_framework import serializers

from .models import KPI, Event, ServiceIndicator, Store, Zone


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "address", "zone"]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "store", "data", "created_at"]


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ["store", "name", "value", "metadata", "category", "date"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIndicator
        fields = ["name", "value", "store", "amount_of_surveys", "date"]
