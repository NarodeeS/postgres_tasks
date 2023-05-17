from datetime import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.cache import cache
from random import randrange

from config import DATABASE_INFO_LIFETIME
from core.models import DatabaseInfo
from postgres_tasks.celery import app
import postgres_tasks.settings as settings
from core.handlers.handlers import delete_db


@app.task
def send_verification_email_task(email: str) -> None:
    verification_number = randrange(1000, 9999)
    cache.set(email, verification_number, 60000)

    html_message = render_to_string('core/email_template.html', {'number_for_verification': verification_number})

    send_mail(
        "Subject here",
        "Here is the message.",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=html_message,
    )


@app.task
def clean_inactive_databases_task() -> None:
    all_databases = DatabaseInfo.objects.all()
    for database in all_databases:
        date_diff = datetime.now() - database.last_action_datetime
        if date_diff.total_seconds() >= DATABASE_INFO_LIFETIME:
            delete_db(database.db_name)
