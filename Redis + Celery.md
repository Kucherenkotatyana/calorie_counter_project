# Redis

```console
docker pull redis
```

```console
docker run --name test-redis -d redis
```

```console
docker exec -it cb9c0362ad4b redis-cli
```

# Redis in Docker Compose

```
redis:  
  image: redis:7.2.3  
  ports:  
    - "6379:6379"
```

```
web:depends_on:redis
```

# Celery Set Up

Install requirements:

```
celery==5.2.7  
django-celery-beat==2.4.0
```

> [!info] https://docs.celeryq.dev/en/4.0/django/first-steps-with-django.html

celery_app.py

```python
import os  
  
from celery import Celery  
  
# Set the default Django settings module for the 'celery' program.  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Calorie_counter.settings')  
  
app = Celery('Calorie_counter')  
  
# Using a string here means the worker doesn't have to serialize  
# the configuration object to child processes.  
# - namespace='CELERY' means all celery-related configuration keys  
#   should have a `CELERY_` prefix.  
app.config_from_object('django.conf:settings', namespace='CELERY')  
  
# Load task modules from all registered Django apps.  
app.autodiscover_tasks()
```

init

```python
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_app import app as celery_app

__all__ = ('celery_app',)
```

settings.py

```python
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER", "redis://redis:6379/0")  
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379/1")
```

# Creation of scheduled task

activity/tasks.py

```python
from celery import shared_task  
from celery.utils.log import get_task_logger  
  
  
logger = get_task_logger("celery_logger")  
  
  
@shared_task()  
def test_scheduled_task():  
    logger.info("test_scheduled_task")
```

settings.py

```python
from celery.schedules import crontab

# ---

CELERY_BEAT_SCHEDULE = {  
    "test-scheduled-task": {  
        "task": "activity.tasks.test_scheduled_task",  
        "schedule": 30,  
    },  
}
```

> [!info] https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules

docker-compose

```
celery:  
  build:  
    context: .  
    dockerfile: Dockerfile  
  entrypoint: "celery -A Calorie_counter.celery_app worker -l info"  
  depends_on:  
    - web  
    - redis  
  env_file:  
    - ./.env  
  volumes:  
    - .:/app  
    - db_data_tmp:/run/mysqld  
  
celery-beat:  
  build:  
    context: .  
    dockerfile: Dockerfile  
  entrypoint: "celery -A Calorie_counter.celery_app beat -l info -s /tmp/celerybeat-schedule"  
  depends_on:  
    - web  
    - redis  
  env_file:  
    - ./.env  
  volumes:  
    - .:/app  
    - db_data_tmp:/run/mysqld
```


# Logging

```python
# LOGGING  
  
LOGGING = {  
    "version": 1,  
    "disable_existing_loggers": False,  
    "formatters": {  
        "verbose": {"format": "%(levelname)s || %(asctime)s || %(module)s: %(message)s"},  
    },  
    "handlers": {  
        "console": {  
            "level": "DEBUG",  
            "class": "logging.StreamHandler",  
            "formatter": "verbose",  
        },  
    },  
    "loggers": {  
        "django": {  
            "handlers": ["console"],  
            "level": "WARNING",  
        },  
        "celery_logger": {  
            "handlers": ["console"],  
            "level": "DEBUG",  
        }  
    },  
}
```

# Sending a task to celery

activity/tasks.py

```python
@shared_task()  
def test_task():  
    logger.debug("test_task")
```

execute

```
from activity.tasks import test_task

test_task.delay()
```