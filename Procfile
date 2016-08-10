web: gunicorn config.wsgi:application
worker: celery worker --app=referral_platform.taskapp --loglevel=info
