from django.conf import settings
from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["email", "given_name", "family_name", "picture"]