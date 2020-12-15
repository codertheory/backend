from django import template, forms

register = template.Library()


@register.filter(is_safe=True)
def find_upload_field_id(form: forms.Form):
    for field in form:
        if isinstance(field.field, forms.FileField):
            return field.auto_id


@register.filter(is_safe=True)
def find_upload_field_label_text(form: forms.Form):
    for field in form:
        if isinstance(field.field, forms.FileField):
            return field.label
