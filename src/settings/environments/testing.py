from src.settings.components.drf import REST_FRAMEWORK

TESTING = True

# to not specify format or content_type in  tests
REST_FRAMEWORK["TEST_REQUEST_DEFAULT_FORMAT"] = "json"

# email
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
