from django.urls import path

from backend.docs.views import openapi_spec, redoc_docs, swagger_ui_docs

urlpatterns = [
    path("openapi.json", openapi_spec, name="openapi_spec"),
    path("", swagger_ui_docs, name="swagger_ui_docs"),
    path("redoc/", redoc_docs, name="redoc_docs"),
]
