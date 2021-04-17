from django.urls import path

from backend.example.v1.views import nice

urlpatterns = [path("nice/", nice, name="nice")]
