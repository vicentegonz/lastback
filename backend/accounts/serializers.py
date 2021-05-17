from rest_framework import serializers

from .models import Device, User


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device

        fields = [
            "user",
            "android_id",
            "ios_id",
            "expo_push_token",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "given_name",
            "family_name",
            "picture",
            "role",
            "stores",
        ]
