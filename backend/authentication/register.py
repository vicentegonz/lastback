from backend.accounts.models import User


def register_social_user(email, given_name, family_name, picture):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        registered_user = User.objects.get(email=email)
        return registered_user.generate_tokens()

    user = {
        "email": email,
        "given_name": given_name,
        "family_name": family_name,
        "picture": picture,
    }
    user = User.objects.create_user(**user)
    user.save()

    return user.generate_tokens()
