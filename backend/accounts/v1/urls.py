from django.urls import path

from .views import UserDetail

urlpatterns = [
    path("", UserDetail.as_view()),
]
