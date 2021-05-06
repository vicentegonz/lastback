from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import GoogleSocialAuthView

urlpatterns = [
    path("google/", GoogleSocialAuthView.as_view(), name="login"),
    path("token/validate/", TokenVerifyView.as_view(), name="token_validation"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
