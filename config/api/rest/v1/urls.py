from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from codertheory.polls.api import views as poll_views
from codertheory.shiritori.api import views as shiritori_views

app_name = "api_version_1"

if settings.DEBUG:
    router = DefaultRouter()
    router.include_root_view = False
else:
    router = SimpleRouter()

router.register("shiritori", shiritori_views.GameModelViewSet, basename="shiritori_game")
router.register("polls", poll_views.PollViewSet, basename="polls")

urlpatterns = router.urls
