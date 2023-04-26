python /server/manage.py makemigrations &&
python /server/manage.py migrate &&
# python /server/manage.py runserver 0.0.0.0:8000
yes yes | python /server/manage.py collectstatic &&
gunicorn --workers 2 --bind 0.0.0.0:8000 postgres_tasks.wsgi:application