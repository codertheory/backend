from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

app_name = "api"

api_info = openapi.Info(
    title="CoderTheory API",
    default_version='v1',
    description="Test description",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="admin@codertheory.dev"),
    license=openapi.License(name="MIT License"),
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# API URLS
urlpatterns = [
    # DRF auth token
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'<str:format>', schema_view.without_ui(cache_timeout=0),
         name='schema-json'),
    path('redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('v1/', include("config.api.rest.v1.urls", namespace="api_version_1"))
]
