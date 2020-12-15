# Create your models here.
import star_ratings.models as ratings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from codertheory.general.models import BaseModel

__all__ = (
    "ChangeLogEntryType",
    "ChangeLogDiffType",
    "ProjectStatus",
    "Project",
    "MobileProject",
    "ProjectFeature",
    "ProjectImage",
    "ProjectFeedBack",
    "ProjectChangeLog",
    "ProjectChangeLogEntry",
    "ProjectChangeLogFiledDiff",
)

User = get_user_model()


class ChangeLogEntryType(models.TextChoices):
    FEATURE = "Feature", _("Feature")
    IMPROVEMENT = "Improvement", _("Improvement")
    FIX = "Fix", _("Fix")


class ChangeLogDiffType(models.TextChoices):
    NEW = "New", _("New")
    UPDATED = "Updated", _("Updated")
    REMOVED = "Removed", _("Removed")


class ProjectStatus(models.TextChoices):
    UNACTIVE = "UnActive", _("Unactive")
    ACTIVE = "Active", _("Active")
    ARCHIVED = "Archived", _("Archived")
    BACKLOG = "Backlog", _("Backlog")


class Project(BaseModel):
    name = models.CharField(max_length=125)
    slug = models.SlugField(null=True, max_length=15)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(blank=True, auto_now_add=True)
    last_updated_at = models.DateTimeField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    current_version = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=25, choices=ProjectStatus.choices, default=ProjectStatus.UNACTIVE)

    class Meta:
        indexes = [
            models.Index(fields=['name', '-created_at', '-last_updated_at'])
        ]

    def __str__(self):
        return self.slug or self.name


class MobileProject(Project):
    logo = models.ImageField(null=True)
    thumbnail = models.ImageField(width_field=360, height_field=590)
    app_store_url = models.URLField(null=True)
    play_store_url = models.URLField(null=True)


class ProjectFeature(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]


class ProjectImage(BaseModel):
    image = models.ImageField(width_field=360, height_field=590)
    posted = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class ProjectFeedBack(BaseModel):
    comment = models.TextField()
    rating = ratings.Rating()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_created=True)

    class Meta:
        indexes = [
            models.Index(fields=['-posted_at'])
        ]


class ProjectChangeLog(BaseModel):
    version = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    updated_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['version'])
        ]


class ProjectChangeLogEntry(BaseModel):
    project = models.ForeignKey(ProjectChangeLog, on_delete=models.CASCADE)
    type = models.CharField(max_length=25, choices=ChangeLogEntryType.choices)
    description = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['type'])
        ]


class ProjectChangeLogFiledDiff(BaseModel):
    filename = models.TextField()
    type = models.CharField(max_length=25, choices=ChangeLogDiffType.choices)
    project = models.ForeignKey(ProjectChangeLog, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['type'])
        ]
