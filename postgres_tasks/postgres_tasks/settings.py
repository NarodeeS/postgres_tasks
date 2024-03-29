from pathlib import Path

import config


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config.DJANGO_SECRET_KEY
DEBUG = config.DEBUG

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
    "minio_storage",
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

# без этого миграции не робят
PROMETHEUS_EXPORT_MIGRATIONS = False

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

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://localhost', 
                        'http://nginx.localhost', 'https://nginx.localhost']

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
        "USER": config.POSTGRES_USER,
        "PASSWORD": config.POSTGRES_PASSWORD,
        "NAME": "postgres",
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache'
    }
}

# minio configuration
if config.TESTING:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
else:
    DEFAULT_FILE_STORAGE = 'minio_storage.storage.MinioMediaStorage'

MINIO_STORAGE_ENDPOINT = "minio:9000"
MINIO_STORAGE_ACCESS_KEY = config.MINIO_STORAGE_ACCESS_KEY
MINIO_STORAGE_SECRET_KEY = config.MINIO_STORAGE_SECRET_KEY
MINIO_STORAGE_USE_HTTPS = False
MINIO_STORAGE_MEDIA_BUCKET_NAME = 'local-media'
MINIO_STORAGE_AUTO_CREATE_MEDIA_BUCKET = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

EMAIL_HOST = 'smtp-relay.sendinblue.com'
EMAIL_PORT = 587

EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD

EMAIL_TIMEOUT = 60
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False

VERIFICATE_EMAIL = config.VERIFICATE_EMAIL

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
    f"amqp://{config.RABBITMQ_DEFAULT_USER}"
    f":{config.RABBITMQ_DEFAULT_PASS}@rabbitmq:5672"
)

MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
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

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'trace_formatter': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] [%(funcName)s] %(message)s',
            'datefmt': '%H:%M:%S %d.%m.%Y',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'formatter': 'trace_formatter',
            'filename': 'django.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'trace_formatter',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
}
