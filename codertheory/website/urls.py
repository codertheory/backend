from django.urls import path, include

from codertheory.website import views

app_name = "website"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home-view"),
    path("blog", views.BlogListView.as_view(), name="blog-list-view"),
    path("blog/", include("pinax.blog.urls", namespace="pinax_blog")),
    path("about", views.AboutUsView.as_view(), name="about-us-view"),
    path("privacy", views.PrivacyPolicyView.as_view(), name="privacy-policy-view")
]
