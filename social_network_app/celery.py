# celery.py

import os
from social_network_app.celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_network_app.settings')

app = Celery('social_network_app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
