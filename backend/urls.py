"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path

from backend.common.versioning import ALLOWED_VERSIONS

ALLOWED_VERSIONS_STRING = "|".join(ALLOWED_VERSIONS)


urlpatterns = [
    path("", include("backend.common.urls")),
    path("docs/", include("backend.docs.urls")),
    re_path(
        rf"(?P<version>({ALLOWED_VERSIONS_STRING}))/",
        include(
            [
                path("authentication/", include("backend.authentication.urls")),
                path("account/", include("backend.accounts.urls")),
                path("operations/", include("backend.operations.urls")),
                path("forecast/", include("backend.forecast.urls")),
            ]
        ),
    ),
]
