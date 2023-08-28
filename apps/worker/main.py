from apps.worker import celeryconfig, create_app

celery = create_app(celeryconfig)
