web: gunicorn csv_generator.wsgi --log-file -
celery: celery -A csv_generator worker -l info -c 4