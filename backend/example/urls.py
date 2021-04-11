from django.urls import path

from backend.example.views import nice

urlpatterns = [path("nice/", nice, name="nice")]
