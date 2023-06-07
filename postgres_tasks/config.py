import os


DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY") or 'very_secret_key'
DATABASE_INFO_LIFETIME = float(os.getenv('DATABASE_INFO_LIFETIME') or '30')
DEBUG = os.getenv("DEBUG") or '0'

POSTGRES_USER = os.getenv("POSTGRES_USER") or 'postgres'
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

SANDBOX_POSTGRES_DB = os.getenv('SANDBOX_POSTGRES_DB') or 'postgres'
SANDBOX_POSTGRES_HOST = os.getenv('SANDBOX_POSTGRES_HOST') or 'sandbox-postgres'
SANDBOX_POSTGRES_PORT = int(os.getenv('SANDBOX_POSTGRES_PORT') or '5432')

RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER') or 'guest'
RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS') or 'guest'

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
VERIFICATE_EMAIL = bool(int(os.getenv('VERIFICATE_EMAIL') or '0'))

MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_STORAGE_ACCESS_KEY')
MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_STORAGE_SECRET_KEY')

TESTING = bool(int(os.getenv('TESTING') or '0'))
