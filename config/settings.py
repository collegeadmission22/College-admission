import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY / BASIC SETTINGS
# ============================================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "dev-only-secret-key-change-this"
)

DEBUG = os.getenv(
    "DEBUG",
    "True"
).lower() == "true"


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost,.onrender.com"
    ).split(",")
    if host.strip()
]

# Render automatically provides this environment variable
render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")

if render_host and render_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_host)


# ============================================================
# INSTALLED APPS
# ============================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # College Admission application
    "admissions",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # WhiteNoise should remain near the top
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URL CONFIGURATION
# ============================================================

ROOT_URLCONF = "config.urls"


# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",

                # Your project context processor
                "admissions.context_processors.portal_links",
            ],
        },
    },
]


# ============================================================
# WSGI
# ============================================================

WSGI_APPLICATION = "config.wsgi.application"


# ============================================================
# DATABASE - POSTGRESQL
# ============================================================

db_url = os.getenv(
    "DATABASE_URL",
    ""
).strip()

if not db_url:
    raise RuntimeError(
        "DATABASE_URL is missing. "
        "Create a .env file in the project root."
    )


DATABASES = {
    "default": dj_database_url.parse(
        db_url,

        # Keep database connections open for reuse
        conn_max_age=600,

        # Check reused connections
        conn_health_checks=True,

        # False for local PostgreSQL
        # True when production database requires SSL
        ssl_require=os.getenv(
            "DB_SSL_REQUIRED",
            "False"
        ).lower() == "true",
    )
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",

        "OPTIONS": {
            "min_length": 8,
        },
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },

    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },

    {
        "NAME":
            "admissions.validators.StrongPasswordValidator",
    },
]


# ============================================================
# LANGUAGE / TIMEZONE
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# CSS / JS / DESIGN FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


# ============================================================
# MEDIA FILES
#
# All uploaded files are stored inside:
#
# media/
#     courses/
#     colleges/
#     college_logos/
#     college_gallery/
#     online_courses/
#     medical_colleges/
#     leads/
#     brochures/
#     student_documents/
#
# Actual subfolder selection is controlled by
# upload_to= in models.py.
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# STORAGE CONFIGURATION
#
# IMPORTANT:
#
# "default" handles:
# - Course images
# - College images
# - Medical college images
# - Online course images
# - Brochures
# - Lead documents
# - Student documents
#
# "staticfiles" handles:
# - CSS
# - JavaScript
# - Static images
#
# This fixes:
#
# InvalidStorageError:
# Could not find config for 'default' in settings.STORAGES
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# LOGIN / LOGOUT
# ============================================================

LOGIN_URL = "/accounts/login/"

LOGIN_REDIRECT_URL = "/student/dashboard/"

LOGOUT_REDIRECT_URL = "/"


# ============================================================
# WHATSAPP
# ============================================================

WHATSAPP_NUMBER = os.getenv(
    "WHATSAPP_NUMBER",
    "917982530590"
)

WHATSAPP_API_URL = os.getenv(
    "WHATSAPP_API_URL",
    ""
)

WHATSAPP_ACCESS_TOKEN = os.getenv(
    "WHATSAPP_ACCESS_TOKEN",
    ""
)


# ============================================================
# EMAIL
# ============================================================

DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    "admission@collegeadmission.co.in"
)

EMAIL_BACKEND = os.getenv(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend"
)

EMAIL_HOST = os.getenv(
    "EMAIL_HOST",
    ""
)

EMAIL_PORT = int(
    os.getenv(
        "EMAIL_PORT",
        "587"
    )
)

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER",
    ""
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD",
    ""
)

EMAIL_USE_TLS = os.getenv(
    "EMAIL_USE_TLS",
    "True"
).lower() == "true"


# ============================================================
# SMS
# ============================================================

SMS_API_URL = os.getenv(
    "SMS_API_URL",
    ""
)

SMS_AUTH_KEY = os.getenv(
    "SMS_AUTH_KEY",
    ""
)

SMS_SENDER_ID = os.getenv(
    "SMS_SENDER_ID",
    "COLADM"
)


# ============================================================
# PRODUCTION / RENDER SECURITY
# ============================================================

if not DEBUG:

    # Tell Django HTTPS is being handled by reverse proxy
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https"
    )

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = os.getenv(
        "SECURE_SSL_REDIRECT",
        "True"
    ).lower() == "true"

    SECURE_HSTS_SECONDS = int(
        os.getenv(
            "SECURE_HSTS_SECONDS",
            "0"
        )
    )

    CSRF_TRUSTED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "CSRF_TRUSTED_ORIGINS",
            "https://*.onrender.com"
        ).split(",")
        if origin.strip()
    ]