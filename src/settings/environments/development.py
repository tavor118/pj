from src.settings.components.base import INSTALLED_APPS, MIDDLEWARE

INSTALLED_APPS += (
    "django_extensions",
    "debug_toolbar",
)

MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
