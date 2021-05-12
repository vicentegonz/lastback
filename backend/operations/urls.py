from django.urls import path

from .views import StoreDetail, StoreList, ZoneDetail, ZoneList

urlpatterns = [
    path("stores/", StoreList.as_view()),
    path("stores/<int:pk>/", StoreDetail.as_view()),
    path("zones/", ZoneList.as_view()),
    path("zones/<int:pk>/", ZoneDetail.as_view()),
]
