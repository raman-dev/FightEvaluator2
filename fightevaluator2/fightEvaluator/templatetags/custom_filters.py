from django import template
register = template.Library()

@register.filter
def rmscores(value: str):
    return value.replace('_',' ')