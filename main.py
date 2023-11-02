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
    CATCH_WEIGHT = "Catch weight"
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

class Note(SQLModel,table=True):
    id: int = Field(primary_key=True)
    assessment_id: int = Field(foreign_key="assessment.id")
    data: str

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
    #create a sample fighter if none exists
    with Session(engine) as session:
        fighter = session.query(Fighter).first()
        if not fighter:
            #commit first since id's are not generated unless committed
            assessment = Assessment(id=0)
            fighter = Fighter(
                id=0,
                first_name="John",
                last_name="Doe",
                nick_name="The Pussy Destroyer",
                weight_class=WeightClass.LIGHTWEIGHT,
                date_of_birth=date(1994,1,1),
                assessment_id=assessment.id
            )
            session.add(assessment)
            session.add(fighter)
            session.commit()
            session.refresh(fighter)

@app.get("/")
async def index():
    #query my database for the next event
    #check the date of the next event
    #if date is upcoming or today load event from database
    #if not retrieve using scraper and create FightEvent object
    #and create matchup objects for each matchup in the events
    #or do i create an endpoint that scrapes the next event and returns it
    return FileResponse("static/index.html")

#assessmnent require fighter id since they cannot exist without a fighter
@app.get("/assessment/{fighter_id}")
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
            print('\nRETRIEVED FROM DB....\n')
            #grab matchups for current event
            matchups = session.query(MatchUp).filter(MatchUp.event_id == event.id).all()
        print(event)

    return {'event':event,'matchups':matchups}

@app.get("/notes/{assessment_id}")
async def get_notes(assessment_id):
    #get notes for assessment id with session
    notes = None
    with Session (engine) as session:
        notes = session.query(Note).filter(Note.assessment_id == assessment_id).all()
    return list(notes)

@app.post("/notes")
async def create_note(note: Note):
    #add note to database
    print('\nRECEIVED FROM BROWSER\n',note)
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
    return note

@app.get("/fighters/{fighter_id}")
async def get_fighter(fighter_id:int):
    print('getting fighter with id -> ',fighter_id)
    with Session(engine) as session:
        fighter = session.get(Fighter,fighter_id)
        return fighter

@app.get("/assessment_styles.css")
async def assessment_styles():
    return FileResponse("static/styles/assessment_styles.css")

@app.get("/styles.css")
async def styles():
    return FileResponse("static/styles/styles.css")

@app.get("/static/media/{resource_name}")
async def media(resource_name):
    return FileResponse("static/media/"+resource_name)


