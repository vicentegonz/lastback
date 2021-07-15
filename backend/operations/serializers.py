from rest_framework import serializers

from .models import KPI, Event, Product, ServiceIndicator, Store, Zone


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
        fields = [
            "id",
            "store",
            "date",
            "category",
            "net_sale",
            "contribution",
            "transactions",
            "gross_sale",
        ]
        read_only_fields = ["id"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceIndicator
        fields = [
            "id",
            "store",
            "date",
            "amount_of_surveys",
            "nps",
            "amount_nps",
            "experience",
            "amount_experience",
            "kindness",
            "amount_kindness",
            "waiting_time",
            "amount_waiting_time",
            "speed",
            "amount_speed",
            "quality",
            "amount_quality",
            "bathroom",
            "amount_bathroom",
        ]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "description"]
        read_only_fields = ["id"]
