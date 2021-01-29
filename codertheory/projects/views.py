import hmac
from hashlib import sha256

from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from codertheory.projects import models


class ProjectView(generic.DetailView):
    template_name = "../website/templates/website/pages/project.html"
    queryset = models.Project.objects.all()
    context_object_name = "project"


# TODO figure out how to test
@method_decorator(csrf_exempt, "dispatch")
class GithubWebhookView(generic.View):
    http_method_names = ['post']

    def post(self, request, **kwargs):
        # Verify the request signature
        header_signature = request.META.get('HTTP_X_HUB_SIGNATURE_256')
        if header_signature is None:
            return HttpResponseForbidden('Permission denied.')

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha256':
            return HttpResponseServerError('Operation not supported.', status=501)

        mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha256)
        if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
            return HttpResponseForbidden('Permission denied.')

        # Process the GitHub events
        event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

        return HttpResponse(status=200)
