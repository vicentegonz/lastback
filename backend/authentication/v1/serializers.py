from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from . import google
from .register import register_social_user


class GoogleSocialAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def validate_id_token(self, id_token):

        user_data = google.Google.validate(id_token)
        try:
            user_data["sub"]
        except Exception:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data["aud"] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("oops, who are you?")

        user_id = user_data["sub"]
        email = user_data["email"]
        name = user_data["name"]
        provider = "google"

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name
        )
