release: python manage.py migrate
web: daphne config.asgi:application
worker: celery worker --app=config.celery_app --loglevel=info
beat: celery beat --app=config.celery_app --loglevel=info
