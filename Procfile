web: gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A core worker -l info
beat: celery -A core beat -l info
