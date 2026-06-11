from django.middleware.clickjacking import XFrameOptionsMiddleware as DjangoXFrameOptionsMiddleware


class XFrameOptionsMiddleware(DjangoXFrameOptionsMiddleware):
    """Keep X-Frame-Options after django-simpleui removes Django's default path."""
