from django.urls import path

from codertheory.website import views

app_name = "website"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home-view"),
    path("about", views.AboutUsView.as_view(), name="about-us-view"),
    path("privacy", views.PrivacyPolicyView.as_view(), name="privacy-policy-view")
]
