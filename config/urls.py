from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from graphene_django.views import GraphQLView

from config.sitemaps import sitemaps

urlpatterns = [
                  path('graphql', GraphQLView.as_view(graphiql=settings.DEBUG)),
                  path("", include("config.api.rest.urls", namespace="api")),
                  path('grappelli/', include('grappelli.urls')),  # grappelli URLS
                  path(settings.ADMIN_URL, admin.site.urls),
                  path('accounts/', include(('allauth.urls', "allauth"), namespace="allauth")),
                  path("auth/", include('djoser.urls')),
                  path("auth/", include('djoser.urls.authtoken')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.

    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
