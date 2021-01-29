from django import template

register = template.Library()


@register.inclusion_tag("../templates/website/widgets/about-widget.html")
def about_widget():
    return {}


@register.inclusion_tag("../templates/website/widgets/search-widget.html", takes_context=True)
def search_widget(context):
    query = context.request.GET.get('query')
    return {
        "query": query
    }
