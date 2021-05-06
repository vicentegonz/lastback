from django.urls import path

urlpatterns = [
    path("contacts/", ContactView.as_view(), name="contacts")
]