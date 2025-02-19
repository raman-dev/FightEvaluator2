from django import template
register = template.Library()
from datetime import datetime



def toMultiplier(odd):
    if odd > 0:
        return round(1 + odd / 100, 2)
    return round(1 + 100 / abs(odd), 2)

@register.filter
def to_multi_str(odd:int) -> str:
    return str(toMultiplier(odd))

@register.filter
def odds_multi_str(odd:int) -> str:
    multi = str(toMultiplier(odd))
    return multi + f'({odd})'

@register.filter
def rmscores(value: str):
    return value.replace('_',' ')

@register.filter
def put_scores(value:str):
    return value.replace(' ','_')

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
def lookup(dict,key):
    return dict[key]

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
