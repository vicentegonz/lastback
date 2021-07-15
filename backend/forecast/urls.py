from django.urls import path

from .views import ListPredictions

urlpatterns = [
    path("predictions/", ListPredictions.as_view()),
]
