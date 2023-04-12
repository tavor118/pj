from datetime import timedelta

from src.settings.components.base import env

AUTH_USER_MODEL = "users.User"

SITE_ID = 1

# JWT authentication will be used by dj-rest-auth
REST_USE_JWT = True

# dj_rest_auth settings
REST_AUTH = {
    "USE_JWT": True,
    # 'JWT_AUTH_COOKIE': 'my-app-auth',
    # 'JWT_AUTH_REFRESH_COOKIE': 'my-refresh-token',
    "JWT_AUTH_HTTPONLY": False,  # False needed for refresh_token
}

# djangorestframework-simplejwt
ACCESS_TOKEN_LIFETIME = env.int("ACCESS_TOKEN_LIFETIME", 5)  # in minutes
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ["Bearer"],
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ["rest_framework_simplejwt.tokens.AccessToken"],
}


# to use old_password on '/password/change/'
OLD_PASSWORD_FIELD_ENABLED = True
# to keep the user logged in after password change
LOGOUT_ON_PASSWORD_CHANGE = False

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = env("ACCOUNT_EMAIL_SUBJECT_PREFIX", default=None)

# to allow the website to verify the user when the user opens the link
# received in the email
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
LOGIN_URL = env("LOGIN_URL", default="http://localhost:8000/api/auth/login/")

ACCOUNT_LOGOUT_ON_GET = False

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
]
