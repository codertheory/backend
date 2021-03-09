
from django.utils import timezone

from codertheory.shiritori import models
from config import celery_app
import datetime

__all__ = (
    "cleanup_old_games",
)


@celery_app.task()
def cleanup_old_games():
    return models.ShiritoriGame.objects.filter(created_at__lte=timezone.now(),
                                               created_at__gt=timezone.now() - datetime.timedelta(days=1),
                                               started=False).delete()
