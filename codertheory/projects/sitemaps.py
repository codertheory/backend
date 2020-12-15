from django.contrib.sitemaps import Sitemap

from codertheory.projects import models


class ProjectSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return models.Project.objects.filter(status=models.ProjectStatus.ACTIVE)

    def lastmod(self, obj):
        return obj.last_updated_at

    def location(self, obj):
        return '/projects/%s' % (obj.slug)
