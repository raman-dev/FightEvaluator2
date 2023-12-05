from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.templating import Jinja2Templates
from datetime import date
from sqlmodel import Session

from .. import scraper
from ..dependencies import get_session
from ..models import Fighter,WeightClass,Assessment,ImageLinkIn,FighterIn

router = APIRouter()
templates = Jinja2Templates(directory="../templates")

#,session: Session = Depends(get_session)):
@router.patch("/fighters/updateImageLink")
async def update_fighter_imglink(imgLinkIn: ImageLinkIn,session: Session = Depends(get_session)):
    fighter = session.get(Fighter,imgLinkIn.fighter_id)
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    fighter.img_link = imgLinkIn.img_link
    session.commit()
    session.refresh(fighter)
    return {'status':'success','img_link':imgLinkIn.img_link}

@router.get("/fighters/{fighter_id}")
def get_fighter(fighter_id:int,session: Session = Depends(get_session)):
    print('getting fighter with id -> ',fighter_id)
    fighter = session.get(Fighter,fighter_id)
    return fighter


@router.post("/create-fighter")
async def create_fighter(request: Request,fighterIn: FighterIn,session: Session = Depends(get_session)):
    #convert the request body to a json object
    # body = await request.body()
    # print(body,json.loads(body),fighterIn.dict())
    # fighter = Fighter(**fighterIn.dict())
    # print(fighter)
    fighterAssessment = Assessment()
    session.add(fighterAssessment)
    session.commit()
    
    fighterIn.weight_class = WeightClass[fighterIn.weight_class]
    fighter = Fighter(**fighterIn.dict())
    fighter.assessment_id = fighterAssessment.id

    session.add(fighter)
    session.commit()
    session.refresh(fighter)
    # print(fighter)
    return fighter
