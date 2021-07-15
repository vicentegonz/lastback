from django.urls import path

from .views import DeviceListView, UserDetail

urlpatterns = [
    path("", UserDetail.as_view()),
    path("devices/", DeviceListView.as_view()),
]
