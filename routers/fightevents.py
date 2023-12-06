from fastapi import APIRouter,Depends,Request
from fastapi.templating import Jinja2Templates
from datetime import date
from sqlmodel import Session
from .. import scraper
from ..dependencies import get_session
from ..models import FightEvent,MatchUp,Fighter,WeightClass,Assessment

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

@router.get("/")
async def index(request: Request,session: Session = Depends(get_session)):
    #query my database for the next event
    #check the date of the next event
    #if date is upcoming or today load event from database
    #if not retrieve using scraper and create FightEvent object
    #and create matchup objects for each matchup in the events
    # print('request',request.body(),request.cookies,request.headers)
    #or do i create an endpoint that scrapes the next event and returns it
    #return FileResponse("static/index.html")
    # with Session(engine) as session:
    context = {"request":request}
    eventData = next_event(session)
    context['event'] = eventData['event']
    context['matchups'] = eventData['matchups']
    for matchup in context['matchups']:
        if matchup.fighter_a_id == None and matchup.fighter_b_id == None:
            fighter_a_id = getFighterIdByName(session,matchup.fighter_a)
            fighter_b_id = getFighterIdByName(session,matchup.fighter_b)

            if fighter_a_id == -1:
                matchup.fighter_a_id = createFighter(matchup.fighter_a_link,session)
            elif fighter_a_id != -1:
                matchup.fighter_a_id = fighter_a_id
            
            if fighter_b_id == -1:
                matchup.fighter_b_id = createFighter(matchup.fighter_b_link,session)
            elif fighter_b_id != -1:
                matchup.fighter_b_id = fighter_b_id
            session.add(matchup)
            session.commit()
        
    return templates.TemplateResponse("index.html",context)#context

def next_event(session):
    matchups = []
    #find the next upcoming event
    event = session.query(FightEvent).filter(FightEvent.date >= date.today()).first()
    if not event:
        print('no event found')
        #if no event is found scrape the next event and create it
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
    return {'event':event,'matchups':matchups}


def getFighterIdByName(session,name):
    # space_index = name.index(' ')
    names = name.split(' ')
    first_name = scraper.normalizeString(names[0])#unicodedata.normalize('NFD',name[:space_index]).encode('ascii', 'ignore').decode("ascii").lower()
    last_name = "" if len(names) == 1 else scraper.normalizeString(" ".join(names[1:]))#unicodedata.normalize('NFD',name[space_index + 1:]).encode('ascii', 'ignore').decode("ascii").lower()
    #find fighter id by first_name last_name
    fighter = session.query(Fighter).filter(Fighter.first_name == first_name,Fighter.last_name == last_name).first()        
    if fighter:
        print(first_name,last_name,fighter.id)
        return fighter.id
    print(first_name,last_name,-1)
    return -1

def createFighter(link,session):
    #need to query site for fighter data and create fighter object
    fighter_data = scraper.getFighterData(link)
    fighterAssessment = Assessment()

    session.add(fighterAssessment)
    session.commit()
    
    if fighter_data['weight_class'] in WeightClass.__members__:
        fighter_data['weight_class'] = WeightClass[fighter_data['weight_class']]
    fighterObj = Fighter(**fighter_data)
    fighterObj.assessment_id = fighterAssessment.id
    
    session.add(fighterObj)
    session.commit()

    return fighterObj.id