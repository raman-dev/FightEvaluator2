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

class FightEvent(SQLModel,table=True):
    id: int = Field(primary_key=True)
    name: str
    date: date
    location: str
    link: Optional[str]

class MatchUp(SQLModel,table=True):
    id: int = Field(primary_key=True)
    # date: Optional[date]
    weight_class: WeightClass
    fighter_a: str
    fighter_b: str
    #almost always 3 unless main-event or championship fight
    max_rounds: Optional[int]
    #optional foreign key to the fightevent table
    event_id: Optional[int] = Field(default=None, foreign_key="fightevent.id")
    # fighters: List["Fighter"] = Relationship(back_populates="matchup")

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

    # fighters: List["Fighter"] = Relationship(back_populates="assessment")

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
    # matchup: Optional[MatchUp] = Relationship(back_populates="fighters")
    #optional since a fighter may need to still be assessed
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    # assesment: Optional["Assessment"] = Relationship(back_populates="fighters")




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
    #or do i create an endpoint that scrapes the next event and returns it
    return FileResponse("static/index.html")

@app.get("/assessment")
async def index():
    return FileResponse("static/assessment.html")

@app.get("/matchup/")
async def index(fighter_a: int | None = None,fighter_b: int | None = None):
    if fighter_a:
        print('matchup for fighters -> ',fighter_a,fighter_b)  
    return FileResponse("static/matchup.html")



@app.get("/nextevent")
async def next_event():
    
    event = None
    matchups = []
    with Session(engine) as session:
        # using session query the fightevent that is greater than current date
        # event = session.query(FightEvent).all()
        event = session.query(FightEvent).filter(FightEvent.date >= date.today()).first()
        if not event:
        #     #if no event is found scrape the next event and create it
            print('fetching from site....')
            next_event = scraper.getNextEvent(scraper.EVENTS_URL)
            event = FightEvent(**next_event)
            session.add(event)
            session.commit()
            #two commits since id is not created until commit is done
            matchupsRaw = scraper.getEventMatchups(event.link)
            for matchup in matchupsRaw:
                matchup = MatchUp(**matchup)
                matchup.event_id = event.id
                print('----',matchup)
                session.add(matchup)
                matchups.append(matchup)
            session.commit()
        else:
            print('retreived from db....')
            #grab matchups for current event
            matchups = session.query(MatchUp).filter(MatchUp.event_id == event.id).all()
        print(event)
    return {'event':event,'matchups':matchups}

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


