from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .google import Google
from .register import register_social_user


class GoogleSocialAuthSerializer(serializers.Serializer):  # pylint: disable=W0223
    id_token = serializers.CharField()

    @staticmethod
    def validate_id_token(id_token):
        user_data = Google.validate(id_token)
        if "sub" not in user_data:
            raise serializers.ValidationError(
                "The token is invalid or expired. Please login again."
            )

        if user_data.get("aud") != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed("Oops, who are you?")

        return register_social_user(
            email=user_data["email"],
            given_name=user_data["given_name"],
            family_name=user_data["family_name"],
            picture=user_data["picture"],
        )
