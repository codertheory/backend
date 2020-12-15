from django.urls import path

from codertheory.projects import views

app_name = "projects"

urlpatterns = [
    path("<slug:slug>", views.ProjectView.as_view())
]
