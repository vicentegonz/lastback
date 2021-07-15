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

    user = User.objects.create_user(email=email, **user_metadata)
    user.save()

    return user.generate_tokens()
