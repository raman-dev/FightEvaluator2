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


@register.filter
def likelihood_str(likelihood):
    return likelihood[1]

@register.filter
def month_num_to_name(monthNumber):
    monthMap = {
        1:'january',
        2:'february',
        3: 'march',
        4:'april',
        5:'may',
        6:'june',
        7:'july',
        8:'august',
        9:'september',
        10:'october',
        11:'november',
        12:'december'
    }
    return monthMap[monthNumber]
