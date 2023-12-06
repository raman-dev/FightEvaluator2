from fastapi import APIRouter,Depends,Request,HTTPException
from sqlmodel import Session
from dependencies import get_session,get_templates
from models import Fighter,Assessment,AssessmentUpdate,Note
from fastapi.templating import Jinja2Templates


router = APIRouter()
# templates = Jinja2Templates(directory="../templates")


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
    if not notes:
        notes = []
    context['fighter'] = fighter
    context['assessment'] = assessment
    context['notes'] = notes
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
