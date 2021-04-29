from rest_framework import serializers

from backend.accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "given_name", "family_name", "picture"]
