import os


DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or 'very_secret_key'
DATABASE_INFO_LIFETIME = float(os.getenv('DATABASE_INFO_LIFETIME') or '30')
DEBUG = os.getenv("DEBUG")

POSTGRES_USER = os.getenv("POSTGRES_USER") or 'postgres'
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SANDBOX_POSTGRES_DB = os.getenv('POSTGRES_DB') or 'postgres'

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER') or 'guest'
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS') or 'guest'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
VERIFICATE_EMAIL = bool(int(os.getenv('VERIFICATE_EMAIL') or '0'))
