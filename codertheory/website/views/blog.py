from django.utils.functional import cached_property
from pinax.blog.views import BlogIndexView
from view_breadcrumbs import ListBreadcrumbMixin


class BlogListView(ListBreadcrumbMixin, BlogIndexView):
    add_home = False
    context_object_name = "blogs"

    @property
    def model_name_title_plural(self):
        return "News"

    @cached_property
    def list_view_name(self):
        return "website:blog-list-view"
