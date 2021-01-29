from django.urls import path

from codertheory.projects import views

app_name = "projects"

urlpatterns = [
    path("github", views.GithubWebhookView.as_view(), name="github"),
    path("<slug:slug>", views.ProjectView.as_view(), name="project-view"),
]
