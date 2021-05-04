import os

import dj_database_url
import sentry_sdk
from decouple import Config, Csv
from sentry_sdk.integrations import django

config = Config(repository=[])

ENVIRONMENT = config("ENV", default="local")

GIT_COMMIT = config("GIT_COMMIT", "unspecifed")

SENTRY_DSN = config("SENTRY_DSN")

# DSN will be taken from SENTRY_DSN env
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[django.DjangoIntegration()],
    environment=ENVIRONMENT,
    release=GIT_COMMIT,
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

DOMAIN_NAME = config("DOMAIN_NAME", default="localhost")
ADDITIONAL_ALLOWED_HOSTS = config("ADDITIONAL_ALLOWED_HOSTS", cast=Csv())
ALLOWED_HOSTS = [DOMAIN_NAME] + ADDITIONAL_ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    "server.apps.AdminConfig",
    # django
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local
    "server.core",
    "server.api",
    # thirdparty
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "server", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "server.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {}
DATABASES["default"] = dj_database_url.parse(
    config("DATABASE_URL"), conn_max_age=600
)

LOCALE_PATHS = [os.path.join(BASE_DIR, "locale")]

TIME_ZONE = "Europe/Warsaw"
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATICFILES_DIRS = [os.path.join(BASE_DIR, "server", "static_files")]

STATIC_URL = "/backend/assets/static/"
STATIC_ROOT = "/assets/static"

MEDIA_URL = "/backend/assets/media/"
MEDIA_ROOT = "/assets/media"

# NOTE(prmtl): since django is behind nginx which is behind load balancer
# we need to pass original protocol in headers LB -> nginx -> django
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOG_LEVEL = config("LOG_LEVEL", default="INFO", cast=str)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] {module} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "": {"handlers": ["console"], "level": LOG_LEVEL},
        "django": {"handlers": ["console"], "propagate": True},
    },
}
