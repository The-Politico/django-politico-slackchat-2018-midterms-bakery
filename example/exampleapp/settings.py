import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.getenv("SECRET_KEY", "SECRET")

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "foreignform",
    "slackchat",
    "chatrender",
    "slackchatbakery",
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

ROOT_URLCONF = "exampleapp.urls"

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

WSGI_APPLICATION = "exampleapp.wsgi.application"


DATABASES = {}
if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config()
else:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"

#########################
# slackchat serializer settings

SLACKCHAT_SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")
SLACKCHAT_SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")
SLACK_WEBHOOK_VERIFICATION_TOKEN = os.getenv("SLACKCHAT_VERIFICATION_TOKEN")

#########################
# slackchatbakery settings

SLACKCHATBAKERY_SECRET_KEY = ""
SLACKCHATBAKERY_SLACKCHAT_CHANNEL_ENDPOINT = (
    "http://127.0.0.1:8000/slackchat/api/channels/"
)
SLACKCHATBAKERY_AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
SLACKCHATBAKERY_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SLACKCHATBAKERY_AWS_REGION = "us-east-2"
SLACKCHATBAKERY_CLOUDFRONT_ALTERNATE_DOMAIN = ""
SLACKCHATBAKERY_S3_UPLOAD_ROOT = (
    "election-results/2018/live-analysis/midterms/"
)
SLACKCHATBAKERY_WEBHOOK_VERIFICATION_TOKEN = os.getenv(
    "SLACKCHAT_VERIFICATION_TOKEN"
)

##############
# Staging S3 #
##############
SLACKCHATBAKERY_AWS_S3_BUCKET = "staging.interactives.politico.com"
SLACKCHATBAKERY_S3_STATIC_ROOT = (
    "https://s3.amazonaws.com/staging.interactives.politico.com"
)  # noqa

#################
# Production S3 #
#################
# SLACKCHATBAKERY_AWS_S3_BUCKET = 'interactives.politico.com'
# SLACKCHATBAKERY_S3_STATIC_ROOT = 'https://www.politico.com'
