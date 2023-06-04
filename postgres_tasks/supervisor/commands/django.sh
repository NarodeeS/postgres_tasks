python /server/manage.py makemigrations &&
python /server/manage.py migrate &&
yes yes | python /server/manage.py collectstatic &&
# python /server/manage.py runserver 0.0.0.0:8000
gunicorn --workers 2 --bind 0.0.0.0:8000 postgres_tasks.wsgi:application