from pathlib import Path

from config import (DJANGO_SECRET_KEY, DEBUG, 
                    POSTGRES_USER, 
                    POSTGRES_PASSWORD,
                    RABBITMQ_DEFAULT_USER, 
                    RABBITMQ_DEFAULT_PASS)


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = DJANGO_SECRET_KEY

DEBUG = DEBUG

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'rest_framework.authtoken',
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_prometheus",
    "corsheaders",
    "djoser",
    "rest_framework",
    "core",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware"
]

ROOT_URLCONF = "postgres_tasks.urls"

# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://localhost:8080",
# ]
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
#     "http://localhost:8080",
# ]  # If this is used, then not need to use `CORS_ALLOW_ALL_ORIGINS = True`
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     "http://localhost:8000",
#     "http://localhost:8080",
# ]
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://localhost']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core.templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "postgres_tasks.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "django-postgres",
        "PORT": "5432",
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "NAME": "postgres",
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'static'
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# настройки celery
CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_DEFAULT_USER}"
    f":{RABBITMQ_DEFAULT_PASS}@rabbitmq:5672"
)

MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', # change to IsEmailVerified
    ]
}

AUTH_USER_MODEL = 'core.User'

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'core.serializers.UserRegistrationSerializer',
    },
    'PERMISSIONS': {
        'user_delete': ['rest_framework.permissions.IsAdminUser'],
    }
}
