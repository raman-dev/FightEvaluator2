from fastapi import APIRouter,Depends,Request,HTTPException
from sqlmodel import Session
from dependencies import get_session,get_templates
from models import Fighter,Assessment,AssessmentUpdate,Note,MatchUp,FightEvent
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["assessments"],
)


#assessmnent require fighter id since they cannot exist without a fighter
@router.get("/assessment/{fighter_id}")
async def assessment(request: Request,fighter_id: int,session: Session = Depends(get_session),templates: Jinja2Templates = Depends(get_templates)):
    context = {"request":request}
    # context['fighter'] = get_fighter(fighter_id)
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
    #for the latest event
    #search the matchups in the latest event that have the same fighter name
    #grab latest fightevent
    nextFightEvent = session.query(FightEvent).order_by(FightEvent.date.desc()).first()
    #get all matchups in that event
    matchups = session.query(MatchUp).filter(MatchUp.event_id == nextFightEvent.id).all()
    #filter matchups for fighter name
    #get fighter name
    fighter_name = fighter.first_name.capitalize() + " " + fighter.last_name.capitalize()
    #filter matchups for fighter name
    matchups = [matchup for matchup in matchups if fighter_name in matchup.fighter_a or fighter_name in matchup.fighter_b]
    if matchups != []:
        nextMatchup = matchups[0]
        context['nextMatchup'] = {
            'matchup_id': nextMatchup.id,
            'fighter_a': nextMatchup.fighter_a.split(" ")[-1],#only last name
            'fighter_b': nextMatchup.fighter_b.split(" ")[-1],
        }
    if not notes:
        notes = []
    context['fighter'] = fighter
    context['assessment'] = assessment
    context['notes'] = notes
    # context['nextMatchup'] = matchups[0]
    # print(type(assessment.__fields__.keys())
    # context['assessment_keys'] = dict(zip(assessment.__fields__.keys(),assessment.__fields__.keys()))
    return templates.TemplateResponse("assessment.html",context)

@router.get("/assessment/data/{assessment_id}")
async def get_assessment(assessment_id: int,session: Session = Depends(get_session)):
    assessment = session.get(Assessment,assessment_id)
    return assessment

@router.patch("/assessment/update")
async def update_assessment(assessmentUpdate: AssessmentUpdate,session: Session = Depends(get_session)):
    #update assessment in database
    db_assessment = session.get(Assessment,assessmentUpdate.id)
    if not db_assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    assessment_data = assessmentUpdate.dict(exclude_unset=True)
    # print(assessment_data)
    for key, value in assessment_data.items():
        setattr(db_assessment, key, value)
    session.commit()
    session.refresh(db_assessment)
    return db_assessment
