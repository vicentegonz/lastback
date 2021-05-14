from rest_framework import serializers

from .models import Event, Store, Zone


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["address", "zone"]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["store", "data"]
