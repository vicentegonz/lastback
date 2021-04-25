from django.urls import path

from backend.common.views import health_check

urlpatterns = [path("health-check/", health_check, name="health_check")]
