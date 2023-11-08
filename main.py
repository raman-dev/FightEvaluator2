from typing import Optional,List
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from datetime import date
from datetime import datetime
from enum import Enum
import scraper

sqlite_file_name ="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,echo=True, connect_args=connect_args)

app = FastAPI()

class AttributeQualifier(Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

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
    fighter_a_link: Optional[str]
    
    fighter_b: str
    fighter_b_link: Optional[str]
    rounds: Optional[str]
    #almost always 3 unless main-event or championship fight
    max_rounds: Optional[int]
    #optional foreign key to the fightevent table
    event_id: Optional[int] = Field(default=None, foreign_key="fightevent.id")
    # fighters: List["Fighter"] = Relationship(back_populates="matchup")


class AssessmentUpdate(SQLModel):
    id: int
    head_movement: Optional[AttributeQualifier] = None
    gas_tank: Optional[AttributeQualifier] = None
    aggression: Optional[AttributeQualifier] = None
    desire_to_win: Optional[AttributeQualifier] = None
    striking: Optional[AttributeQualifier] = None
    chinny: Optional[AttributeQualifier] = None
    grappling_offense: Optional[AttributeQualifier] = None
    grappling_defense: Optional[AttributeQualifier] = None

class Assessment(SQLModel,table=True):
    id: int = Field(primary_key=True)
    head_movement: Optional[AttributeQualifier]
    gas_tank: Optional[AttributeQualifier]
    aggression: Optional[AttributeQualifier]
    desire_to_win: Optional[AttributeQualifier]
    striking: Optional[AttributeQualifier]
    chinny: Optional[AttributeQualifier]
    grappling_offense: Optional[AttributeQualifier]
    grappling_defense: Optional[AttributeQualifier]

class NoteIn(SQLModel):
    assessment_id: int
    data: str

class Note(SQLModel,table=True):
    id: int = Field(primary_key=True)
    assessment_id: int = Field(foreign_key="assessment.id")
    data: str
    timestamp: str = Field(default=datetime.now().isoformat())

class Fighter(SQLModel,table=True):
    id: int = Field(primary_key=True)
    first_name: str
    last_name: str
    nick_name: Optional[str] 
    weight_class: Optional[WeightClass]
    height: Optional[str]
    date_of_birth: Optional[date]
    #an optional foreign key to the matchup table if a matchup is scheduled
    # matchup_id: Optional[int] = Field(default=None, foreign_key="matchup.id")
    # matchup: Optional[MatchUp] = Relationship(back_populates="fighters")
    #optional since a fighter may need to still be assessed
    assessment_id: Optional[int] = Field(default=None, foreign_key="assessment.id")
    # assesment: Optional["Assessment"] = Relationship(back_populates="fighters")


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def weightclassStr(weightclass: WeightClass):
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

def stripDomain(url):
    return url.replace("https://www.tapology.com","")

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.filters['weightclassStr'] = weightclassStr
templates.env.filters['none2Null'] = none2Null
templates.env.filters['fightAttribQualifier'] = fightAttribQualifier
templates.env.filters['stripDomain'] = stripDomain


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
async def index(request: Request):
    #query my database for the next event
    #check the date of the next event
    #if date is upcoming or today load event from database
    #if not retrieve using scraper and create FightEvent object
    #and create matchup objects for each matchup in the events
    #or do i create an endpoint that scrapes the next event and returns it
    # return FileResponse("static/index.html")
    with Session(engine) as session:
        context = {"request":request}
        eventData = next_event(session)
        context['event'] = eventData['event']
        context['matchups'] = eventData['matchups']
        return templates.TemplateResponse("index.html",context)#context

#assessmnent require fighter id since they cannot exist without a fighter
@app.get("/assessment/{fighter_id}")
async def index(request: Request,fighter_id: int):
    # return FileResponse("static/assessment.html")
    context = {"request":request}
    # context['fighter'] = get_fighter(fighter_id)
    with Session(engine) as session:
        fighter = session.get(Fighter,fighter_id)
        if not fighter:
            raise HTTPException(status_code=404, detail="Fighter not found")
        assessment = session.get(Assessment,fighter.assessment_id)
        if not assessment:
            assessment = Assessment()
            fighter.assessment_id = assessment.id
            session.add(assessment)
            session.commit()
            session.refresh(assessment)
        #get all notes with assessment_id
        notes = session.query(Note).filter(Note.assessment_id == assessment.id).order_by(Note.timestamp.desc()).all()
        if not notes:
            notes = []
        context['fighter'] = fighter
        context['assessment'] = assessment
        context['notes'] = notes
        # print(type(assessment.__fields__.keys())
        # context['assessment_keys'] = dict(zip(assessment.__fields__.keys(),assessment.__fields__.keys()))
    return templates.TemplateResponse("assessment.html",context)

@app.get("/assessment/data/{assessment_id}")
async def get_assessment(assessment_id: int):
    with Session (engine) as session:
        assessment = session.get(Assessment,assessment_id)
        return assessment

@app.patch("/assessment/")
async def update_assessment(assessmentUpdate: AssessmentUpdate):
    #update assessment in database
    with Session(engine) as session:
        db_assessment = session.get(Assessment,assessmentUpdate.id)
        if not db_assessment:
            raise HTTPException(status_code=404, detail="Assessment not found")
        assessment_data = assessmentUpdate.dict(exclude_unset=True)
        for key, value in assessment_data.items():
            setattr(db_assessment, key, value)
        session.commit()
        session.refresh(db_assessment)
        return db_assessment

@app.get("/matchup/")
async def index(fighter_a: int | None = None,fighter_b: int | None = None):
    if fighter_a:
        print('matchup for fighters -> ',fighter_a,fighter_b)  
    return FileResponse("static/matchup.html")

# @app.get("/nextevent")
def next_event(session):
    matchups = []
    event = session.query(FightEvent).filter(FightEvent.date >= date.today()).first()
    if not event:
    #     #if no event is found scrape the next event and create it
        print('fetching from site....')            
        #two commits since id is not created until commit is done
        eventData = scraper.getNextEvent2()
        event = FightEvent(**eventData['event'])
        session.add(event)
        session.commit()
        for matchupRaw in eventData['matchups']:
            matchup = MatchUp(**matchupRaw)
            matchup.event_id = event.id
            session.add(matchup)
            session.commit()
            session.refresh(matchup)
            matchups.append(matchup)
        session.refresh(event)
        return {'event':event,'matchups':matchups}
    else:
        print('\nRETRIEVED FROM DB....\n')
        #grab matchups for current event
        matchups = session.query(MatchUp).filter(MatchUp.event_id == event.id).all()
    # print(event)
    return {'event':event,'matchups':matchups}

@app.get("/notes/{assessment_id}")
async def get_notes(assessment_id):
    #get notes for assessment id with session
    notes = None
    with Session (engine) as session:
        notes = session.query(Note).filter(Note.assessment_id == assessment_id).all()
    return list(notes)

@app.post("/notes")
async def create_note(noteIn: NoteIn):#,request: Request):
    #add note to database
    # body = await request.body()
    # print('\nRECEIVED FROM BROWSER\n',body,noteIn.data)
    note = Note(assessment_id=noteIn.assessment_id,data=noteIn.data,timestamp=datetime.now().isoformat())
    with Session(engine) as session:
        session.add(note)
        session.commit()
        session.refresh(note)
    return note

@app.delete("/notes/{note_id}")
async def delete_notes(note_id):
    #delete note from database
    with Session(engine) as session:
        note = session.get(Note,note_id)
        if not note:
            return {'status':'failed'}
        session.delete(note)
        session.commit()
    return {'status':'success'}


@app.get("/fighters/{fighter_id}")
def get_fighter(fighter_id:int):
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


