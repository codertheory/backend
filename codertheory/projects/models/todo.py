from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from codertheory.general.models import BaseModel
from .applications import Project

__all__ = (
    "TaskStatus",
    "TaskBoard",
    "Task"
)

User = get_user_model()


class TaskStatus(models.TextChoices):
    InProgress = "InProgress", _("InProgress")
    Finished = "Finished", _("Finished")
    Ignored = "Ignored", _("Ignored")


class TaskBoard(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_created=True, auto_now=True)


class Task(BaseModel):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=TaskStatus.choices, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    unread = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)
    board = models.ForeignKey(TaskBoard, on_delete=models.CASCADE, null=True)

    def finish(self):
        if self.finished_at is None:
            self.finished_at = timezone.now()

    def unfinish(self):
        if self.finished_at is not None:
            self.finished_at = None
