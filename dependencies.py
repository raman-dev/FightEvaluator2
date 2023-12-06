from sqlmodel import Field, Session, SQLModel, create_engine, select
from fastapi.templating import Jinja2Templates
from models import WeightClass,AttributeQualifier
from datetime import date,datetime


attribValueStateMap = {
    "head_movement":{"positive":"good","neutral":"mediocre","negative":"bad","untested":"untested"},
    "gas_tank":{"positive":"good","neutral":"mediocre","negative":"bad","untested":"untested"},
    "aggression":{"positive":"high","neutral":"mid","negative":"low","untested":"untested"},
    "striking":{"positive":"good","neutral":"mediocre","negative":"bad","untested":"untested"},
    "chinny":{"positive":"no","neutral":"somewhat","negative":"yes","untested":"untested"},
    "desire_to_win":{"positive":"yes","neutral":"kinda","negative":"no","untested":"untested"},
    "grappling_offense":{"positive":"good","neutral":"mediocre","negative":"bad","untested":"untested"},
    "grappling_defense":{"positive":"good","neutral":"mediocre","negative":"bad","untested":"untested"}
}


sqlite_file_name ="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,connect_args=connect_args)
SQLModel.metadata.create_all(engine)

def weightClassToStr(weightclass: WeightClass):
    return weightclass.value.__str__()

def none2Null(value):
    if value == None:
        return "null"
    else:
        return value

def fightAttribQualifier(value):
    if value == None:
        return "null"
    return '`'+value.value.__str__() +'`'

def attribToStr(value):
    if value == None:
        return "untested"

    return value.value.__str__()

def dobToAge(dob: datetime.date):
    if dob == None:
        return "N\A"
    today = date.today()
    if today == None:
        return "FUCK YOU"
    return (today - dob).days // 365

def attribNameToStr(attribName):
    result = attribName.replace("_"," ")
    return result.title()

def attribToStateStr(attribName: str,attribValue: AttributeQualifier):
    if not attribValue:
        return "untested"
    return attribValueStateMap[attribName][attribValue.name]

def fightLinkFilter(link:str):
    if link == None:
        return "null"
    return '`' + link+ '`'

templates = Jinja2Templates(directory="templates")
templates.env.filters['weightClassToStr'] = weightClassToStr
templates.env.filters['none2Null'] = none2Null
templates.env.filters['fightAttribQualifier'] = fightAttribQualifier
templates.env.filters['dobToAge'] = dobToAge
templates.env.filters['attribToStr'] = attribToStr
templates.env.filters['attribNameToStr'] = attribNameToStr
templates.env.filters['attribToStateStr'] = attribToStateStr
templates.env.filters['fightLinkFilter'] = fightLinkFilter

async def get_templates():
    return templates


async def get_session():
    with Session(engine) as session:
        yield session

async def get_engine():
    return engine