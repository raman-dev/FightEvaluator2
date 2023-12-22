from django import template


register = template.Library()

# @register.filter
# def tojson(instance):
#     return instance.to_json()