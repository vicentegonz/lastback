import os
import json

from django.conf import settings
from django.shortcuts import render

from backend.docs.responses import AttachmentJsonResponse


def openapi_spec(_):
    spec_location = os.path.join(settings.BASE_DIR, "docs", "openapi.json")
    with open(spec_location, "r") as spec_file:
        spec = json.load(spec_file)
    return AttachmentJsonResponse(spec, "openapi")


def redoc_docs(request):
    return render(request, "redoc.html")


def swagger_ui_docs(request):
    return render(request, "swagger-ui.html")
