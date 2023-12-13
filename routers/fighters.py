from fastapi import APIRouter,Depends,Request,HTTPException
from fastapi.templating import Jinja2Templates
from datetime import date
from sqlmodel import Session

from dependencies import get_session,get_templates
from models import Fighter,WeightClass,Assessment,ImageLinkIn,FighterIn,FighterUpdateIn,FighterSearchOut

router = APIRouter(
    tags=["fighters"],
)


@router.patch("/fighters/update/image-link")
async def update_fighter_imglink(imgLinkIn: ImageLinkIn,session: Session = Depends(get_session),templates: Jinja2Templates = Depends(get_templates)):
    fighter = session.get(Fighter,imgLinkIn.fighter_id)
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    fighter.img_link = imgLinkIn.img_link
    session.commit()
    session.refresh(fighter)
    return {'status':'success','img_link':imgLinkIn.img_link}

@router.patch("/fighters/update-fighter")
async def update_fighter(fighterIn: FighterUpdateIn, session: Session = Depends(get_session)):
    fighter = session.get(Fighter,fighterIn.id)
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    #update fighter object if fighterIn key exists
    fighterUpdateDict = fighterIn.dict()
    for inkey in fighterUpdateDict.keys():
        if fighterUpdateDict[inkey] != None:
            if inkey == 'weight_class':
                fighterUpdateDict['weight_class'] = WeightClass[fighterIn.weight_class]
            setattr(fighter,inkey,fighterUpdateDict[inkey])
    session.commit()
    session.refresh(fighter)
    return fighter
 
@router.get("/fighters/{fighter_id}")
def get_fighter(fighter_id:int,session: Session = Depends(get_session),templates: Jinja2Templates = Depends(get_templates)):
    print('getting fighter with id -> ',fighter_id)
    fighter = session.get(Fighter,fighter_id)
    return fighter


@router.post("/fighters/create-fighter")
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

# @app.get("/predict")
# async def predictUI(request: Request):
#     context = {"request":request}
#     return templates.TemplateResponse("predict.html",context)

@router.get("/fighters/search/",response_model=list[FighterSearchOut])
async def search(request: Request,search: str,session: Session = Depends(get_session)):
    terms = search.split(' ')
    print('search.terms => ',terms)
    fname = terms[0]
    lname = fname
    if len(terms) > 1:
        lname = terms[1]
    # with Session(engine) as session:
        """
            fname == lname then
            if not do fname and lname search
        """
    fighters = []
    if fname == lname:
        fighters = session.query(Fighter).filter(Fighter.first_name.contains(fname) | Fighter.last_name.contains(lname)).limit(5).all()
    else:
        fighters = session.query(Fighter).filter(Fighter.first_name.contains(fname),Fighter.last_name.contains(lname)).limit(5).all()
    return [FighterSearchOut(fighter_id=fighter.id,first_name=fighter.first_name,last_name=fighter.last_name,weight_class=fighter.weight_class) for fighter in fighters]