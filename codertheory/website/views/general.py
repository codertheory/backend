from django.contrib.auth import get_user_model
from django.views import generic

from codertheory.users import models as user_models
from .. import models


# Create your views here.


class HomeView(generic.ListView):
    template_name = 'website/pages/index.html'
    context_object_name = "banners"
    queryset = models.DisplayBanner.objects.filter(active=True)


class AboutUsView(generic.ListView):
    template_name = "website/pages/about.html"
    context_object_name = "staff_members"

    def get_queryset(self):
        user_model: user_models.User = get_user_model()
        return user_model.objects.filter(is_staff=True)


class PrivacyPolicyView(generic.TemplateView):
    template_name = "website/pages/privacy.html"
