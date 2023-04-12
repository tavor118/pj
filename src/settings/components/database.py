# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

from src.settings.components.base import env

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="pythonjunior"),
        "USER": env("DB_USER", default="postgres"),
        "PASSWORD": env("DB_PASSWORD", default=""),
        "HOST": env("DB_HOST", default="127.0.0.1"),
        "PORT": env.int("DB_PORT", default=5432),
        "CONN_MAX_AGE": 3600,
    }
}
