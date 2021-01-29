import calendar
import datetime

from allauth.socialaccount.templatetags.socialaccount import get_providers
from django import template

register = template.Library()


@register.inclusion_tag(filename="favicon.html", takes_context=True)
def favicon(context):
    return {}


@register.inclusion_tag(filename="../templates/website/components/breadcrumbs.html",
                        takes_context=True)
def breadcrumbs(context, *args):
    pass


@register.inclusion_tag(filename="../templates/website/components/blogs/blog-preview.html")
def article_preview(article):
    return {"article": article}


@register.filter(is_safe=True)
def month_name(month):
    if month:
        return calendar.month_name[month]
    else:
        return ""


@register.filter(is_safe=True)
def day_name(dt: datetime.datetime):
    return calendar.day_name[dt.weekday()]


@register.simple_tag
def provider_exists(provider: str) -> bool:
    providers = get_providers()
    return provider in providers
