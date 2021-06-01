from rest_framework import serializers

from .models import KPI, Event, Store, Zone


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
        fields = ["name", "value", "store", "timestamp"]
