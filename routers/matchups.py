from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.templating import Jinja2Templates
from datetime import date
from sqlmodel import Session

from dependencies import get_session,get_templates
from models import MatchUp,Fighter,WeightClass,Assessment,Note,MatchupIn

router = APIRouter()
# templates = Jinja2Templates(directory="../templates")

@router.get("/matchup/{matchup_id}")
async def index(request: Request,matchup_id: int,session: Session = Depends(get_session),templates: Jinja2Templates = Depends(get_templates)):
    matchup = session.get(MatchUp,matchup_id)
    if not matchup:
        raise HTTPException(status_code=404, detail="Matchup not found")
    fighter_a = session.get(Fighter,matchup.fighter_a_id)
    fighter_b = session.get(Fighter,matchup.fighter_b_id)
    context = {'request': request}
    context['matchup'] = matchup
    context['fighter_a'] = {
        'data':fighter_a,
        'assessment':session.get(Assessment,fighter_a.assessment_id),
        'notes' : session.query(Note).filter(Note.assessment_id == fighter_a.assessment_id).order_by(Note.timestamp.desc()).all()
    }
    context['fighter_b'] = {
        'data':fighter_b,
        'assessment':session.get(Assessment,fighter_b.assessment_id),
        'notes' : session.query(Note).filter(Note.assessment_id == fighter_b.assessment_id).order_by(Note.timestamp.desc()).all()
    }
    return templates.TemplateResponse("matchup.html",context)


@router.post("/create-matchup")
async def create_matchup(request: Request,matchupIn: MatchupIn,session: Session = Depends(get_session)):
    #convert the request body to a json object
    # print(matchupIn.dict())
    
    fighterA = session.get(Fighter,matchupIn.fighter_a_id)
    fighterB = session.get(Fighter,matchupIn.fighter_b_id)
    matchup = MatchUp(
        event_id=matchupIn.event_id,
        fighter_a_id=matchupIn.fighter_a_id,
        fighter_a=fighterA.first_name+' '+fighterA.last_name,
        fighter_b_id=matchupIn.fighter_b_id,
        fighter_b=fighterB.first_name+' '+fighterB.last_name,
        weight_class=WeightClass[matchupIn.weight_class.upper()]
        )
    session.add(matchup)
    session.commit()
    session.refresh(matchup)
    return matchup
    # return {'status':'success'}
    
@router.delete("/delete-matchup/{matchup_id}")
async def delete_matchup(matchup_id: int,session: Session = Depends(get_session)):
    matchup = session.get(MatchUp,matchup_id)
    if not matchup:
        raise HTTPException(status_code=404, detail="Matchup not found")
    session.delete(matchup)
    session.commit()
    return {'status':'success'}
