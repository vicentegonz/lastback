from django.urls import path

from .views import (
    CreateEvents,
    KPICreate,
    ListEvents,
    ListKPI,
    ServiceIndicatorCreate,
    ServiceIndicatorList,
    StoreDetail,
    StoreList,
    ZoneDetail,
    ZoneList,
)

urlpatterns = [
    path("stores/", StoreList.as_view()),
    path("stores/<int:pk>/", StoreDetail.as_view()),
    path("stores/events/", CreateEvents.as_view()),
    path("stores/<int:pk>/events/", ListEvents.as_view()),
    path("stores/<int:pk>/kpis/", ListKPI.as_view()),
    path("stores/<int:pk>/service-indicators/", ServiceIndicatorList.as_view()),
    path("kpis/", KPICreate.as_view()),
    path("service-indicators/", ServiceIndicatorCreate.as_view()),
    path("zones/", ZoneList.as_view()),
    path("zones/<int:pk>/", ZoneDetail.as_view()),
]
