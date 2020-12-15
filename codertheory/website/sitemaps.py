from django.contrib.sitemaps import Sitemap
from pinax.blog import models


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'http'

    def items(self):
        return models.Post.objects.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return '/blog/%s' % (obj.slug)
