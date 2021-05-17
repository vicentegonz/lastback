from rest_framework.versioning import URLPathVersioning

ALLOWED_VERSIONS = ["v1"]


class VersioningClass(URLPathVersioning):
    default_version = "v1"
    allowed_versions = ALLOWED_VERSIONS


class VersioningMixin:
    versioning_class = VersioningClass
