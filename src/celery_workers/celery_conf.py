from celery import Celery
from celery.schedules import crontab
from celery.signals import setup_logging

from core.config import settings

app = Celery("celery_workers", broker=settings.redis.broker_url)

app.conf.beat_schedule = {
    "Check-every-minute": {
        "task": "celery_workers.tasks.tokens_expired_checker",
        "schedule": crontab(minute=f"*/{1}"),
    }
}


@setup_logging.connect()
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig

    dictConfig(app.config["LOGGING_CONFIG"])


app.autodiscover_tasks(["celery_workers"])
