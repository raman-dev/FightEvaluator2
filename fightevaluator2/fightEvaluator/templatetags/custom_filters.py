from django import template
register = template.Library()
from datetime import datetime

@register.filter
def rmscores(value: str):
    return value.replace('_',' ')

@register.filter
def toage(value: datetime.date):
    if not value:
        return ""
    #convert datetime.date to age 
    today = datetime.now().date()
    age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    return age

@register.filter
def height_str(value: int):
    if not value:
        return None
    return f'{value // 12}\'{value % 12}'
