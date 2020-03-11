from typing import Dict

import os


from .settings_external import get, getboolean
from .settings_auth import AUTH_INFO

from .settings_auth import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get("global", "secret_key", "SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getboolean("global", "debug", "DEBUG")

ALLOWED_HOSTS = [
    x.strip() for x in get("global", "allowed_hosts", "ALLOWED_HOSTS").split()
]

# Application definition

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + AUTH_INFO["installed_apps"]
    + ["rest_framework", "rules.apps.AutodiscoverRulesConfig", "zezere"]
)

REST_FRAMEWORK = {}
if AUTH_INFO.get("drf_default_authentication_classes"):  # pragma: no cover
    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = AUTH_INFO[
        "drf_default_authentication_classes"
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "zezere.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "zezere.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES: Dict[str, Dict[str, str]] = {"default": {}}

for default_key in ("engine", "name", "user", "password", "host", "port"):
    val = get("database", default_key, "DATABASE_%s" % default_key)
    if val:
        DATABASES["default"][default_key.upper()] = val

print(DATABASES)

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

main_auth_backend = None


AUTHENTICATION_BACKENDS = AUTH_INFO["backends"] + (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"

secheadername = get("secure_proxy_ssl_header", "header", "SECURE_PROXY_SSL_HEADER_NAME")
secheadervalue = get(
    "secure_proxy_ssl_header", "value", "SECURE_PROXY_SSL_HEADER_VALUE"
)
SECURE_PROXY_SSL_HEADER = (secheadername, secheadervalue) if secheadername else None
