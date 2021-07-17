from django.urls import path

from .views import CreateRecommendation, ListPredictions

urlpatterns = [
    path("predictions/", ListPredictions.as_view()),
    path("recommendations/", CreateRecommendation.as_view()),
]
