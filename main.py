from typing import Optional,List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import date
from enum import Enum
import scraper

sqlite_file_name ="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,echo=True, connect_args=connect_args)

app = FastAPI()

class AttributeQualifier(Enum):
    good = "good"
    bad = "bad"
    mediocre = "mediocre"
    high = "high"
    mid = "mid"
    low = "low"

class WeightClass(Enum):
    CATCHWEIGHT = "Catchweight"
    STRAWWEIGHT = "Strawweight"
    FLYWEIGHT = "Flyweight"
    BANTAMWEIGHT = "Bantamweight"
    FEATHERWEIGHT = "Featherweight"
    LIGHTWEIGHT = "Lightweight"
    WELTERWEIGHT = "Welterweight"
    MIDDLEWEIGHT = "Middleweight"
    LIGHT_HEAVYWEIGHT = "Light Heavyweight"
    HEAVYWEIGHT = "Heavyweight"

class MatchUp(SQLModel,table=True):
    id: int = Field(primary_key=True)
    date: Optional[date]
    max_rounds: int
    weight_class: WeightClass

class Fighter(SQLModel,table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    nick_name: Optional[str] 
    weight_class: Optional[WeightClass]
    height: Optional[str]
    date_of_birth: Optional[date]
    #an optional foreign key to the matchup table if a matchup is scheduled
    matchup_id: Optional[int] = Field(default=None, foreign_key="matchup.id")
    matchup: Optional[MatchUp] = Relationship(back_populates="fighters")
    #optional since a fighter may need to still be assessed
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    assesment: Optional["Assessment"] = Relationship(back_populates="fighter")


class Assessment(SQLModel,table=True):
    id: int = Field(primary_key=True)
    head_movement: Optional[AttributeQualifier]
    gas_tank: Optional[AttributeQualifier]
    aggression: Optional[AttributeQualifier]
    desire_to_win: Optional[AttributeQualifier]
    striking: Optional[AttributeQualifier]
    chinny: Optional[bool]
    grappling_offense: Optional[AttributeQualifier]
    grappling_defense: Optional[AttributeQualifier]
    notes: Optional[str]

class FightEvent(SQLModel,table=True):
    id: int = Field(primary_key=True)
    name: str
    date: date
    location: str


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
# templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_start():
    create_db_and_tables()
    # create_sample_data()

@app.get("/")
async def index():
    #query my database for the next event
    #check the date of the next event
    #if date is upcoming or today load event from database
    #if not retrieve using scraper and create FightEvent object
    #and create matchup objects for each matchup in the events
    return FileResponse("static/index.html")

@app.get("/assessment")
async def index():
    return FileResponse("static/assessment.html")

@app.get("/matchup")
async def index():
    return FileResponse("static/matchup.html")

@app.get("/styles.css")
async def styles():
    return FileResponse("static/styles/styles.css")

@app.get("/static/media/{resource_name}")
async def media(resource_name):
    return FileResponse("static/media/"+resource_name)

@app.get("/fighters/{fighter_id}")
async def get_fighter(fighter_id:int):
    with Session(engine) as session:
        fighter = session.get(Fighter,fighter_id)
        return fighter


