import os

from celery import Celery
from django.conf import settings

#TODO Change this in production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'azubisc.settings.local')

app = Celery('azubisc')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
