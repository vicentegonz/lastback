from rest_framework import serializers

from .models import Store, Zone


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["address", "zone"]


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["name"]
