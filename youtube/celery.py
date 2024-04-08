import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube.settings")

app = Celery("youtube")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from core.tasks import FetchYTVideoPeriodicTask

schedule = dict()
task_list = [
    FetchYTVideoPeriodicTask,
]
for task in task_list:
    schedule[task.name] = {
        "task": task.name,
        "schedule": task.run_every,
        "args": (),
    }

app.conf.beat_schedule = schedule
