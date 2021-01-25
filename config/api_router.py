from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter, SimpleRouter


app_name = "api"

api_info = openapi.Info(
    title="CoderTheory API",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="admin@codertheory.com"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:
    router = DefaultRouter()
    router.include_root_view = False
else:
    router = SimpleRouter()


# noinspection PyUnresolvedReferences
urlpatterns = [
                  path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  path(r'<str:format>', schema_view.without_ui(cache_timeout=0),
                       name='schema-json'),
                  path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
              ] + router.urls + order_item_router.urls
