from django.contrib.auth import get_user_model
from django.views import generic

from codertheory.projects import models as project_models
from codertheory.users import models as user_models
from codertheory.website import models as website_models

__all__ = (
    "HomeView",
    "AboutUsView",
    "PrivacyPolicyView",
)


# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'website/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['banners'] = website_models.DisplayBanner.objects.filter(active=True)[:5]
        context['project_stats'] = {
            "lines": 5000,
            "projects": 2300,
        }
        context['mobile_projects'] = project_models.MobileProject.objects.filter(status=project_models.ProjectStatus.ACTIVE)[:3]
        return context


class AboutUsView(generic.ListView):
    template_name = "website/pages/about.html"
    context_object_name = "staff_members"

    def get_queryset(self):
        user_model: user_models.User = get_user_model()
        return user_model.objects.filter(is_staff=True)


class PrivacyPolicyView(generic.TemplateView):
    template_name = "website/pages/privacy.html"
