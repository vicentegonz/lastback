from rest_framework.exceptions import AuthenticationFailed

from backend.accounts.models import User


def register_social_user(email, given_name, family_name, picture):
    filtered_user_by_email = User.objects.filter(email=email)

    user_metadata = {
        "given_name": given_name,
        "family_name": family_name,
        "picture": picture,
    }

    if filtered_user_by_email.exists():
        filtered_user_by_email.update(**user_metadata)
        user = User.objects.get(email=email)
        return user.generate_tokens()

    raise AuthenticationFailed("Oops, who are you?")
