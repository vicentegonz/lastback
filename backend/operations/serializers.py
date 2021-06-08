from rest_framework import serializers

from .models import KPI, Event, ServiceIndicator, Store, Zone


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "address", "zone"]
        read_only_fields = ["id"]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name"]
        read_only_fields = ["id"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "store", "data", "created_at"]
        read_only_fields = ["id"]


class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ["id", "name", "value", "store", "category", "date", "metadata"]
        read_only_fields = ["id"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIndicator
        fields = ["id", "name", "value", "store", "amount_of_surveys", "date"]
        read_only_fields = ["id"]
