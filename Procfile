release: python manage.py migrate
web: daphne config.asgi:application --port $PORT --bind 0.0.0.0
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
