# Register your models here.
from django.contrib import admin

from codertheory.projects import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MobileProject)
class MobileProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectFeedBack)
class ProjectFeedBackAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectChangeLog)
class ProjectChangeLogAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProjectChangeLogEntry)
class ProjectChangeLogEntryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaskBoard)
class TaskBoardAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    pass
