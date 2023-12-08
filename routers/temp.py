from fastapi import APIRouter,Depends
from datetime import datetime
from sqlmodel import Session
from dependencies import get_session
from models import TempMatchUp,MatchUp,WeightClass


# router = APIRouter(
#     tags=["temp"],
# )



# @router.get("/temp")
# async def get_temp(session: Session = Depends(get_session)):
#     #create a temp object
#     temp = TempMatchUp()
#     temp.fighter_a = "test"
#     temp.fighter_b = "test"
#     temp.weight_class = WeightClass.FLYWEIGHT
#     temp.event_id = 1

#     session.add(temp)
#     session.commit()
#     return {'status':'success'}

# @router.get("/temp/copy-matchups")
# async def copy_matchups(session: Session = Depends(get_session)):
#     matchups = session.query(MatchUp).all()
#     for matchup in matchups:
#         temp = TempMatchUp()
#         temp.fighter_a = matchup.fighter_a
#         temp.fighter_a_link = matchup.fighter_a_link
#         temp.fighter_a_id = matchup.fighter_a_id
#         temp.fighter_b = matchup.fighter_b
#         temp.fighter_b_link = matchup.fighter_b_link
#         temp.fighter_b_id = matchup.fighter_b_id
#         temp.weight_class = matchup.weight_class
#         temp.event_id = matchup.event_id
#         temp.rounds = matchup.rounds
#         temp.max_rounds = matchup.max_rounds
#         session.add(temp)
#     session.commit()
#     return {'status':'success'}

# @router.get("/temp/copy-matchups-back")
# async def copy_matchups_back(session: Session = Depends(get_session)):
#     matchups = session.query(TempMatchUp).all()
#     for matchup in matchups:
#         temp = MatchUp()
#         temp.fighter_a = matchup.fighter_a
#         temp.fighter_a_link = matchup.fighter_a_link
#         temp.fighter_a_id = matchup.fighter_a_id
#         temp.fighter_b = matchup.fighter_b
#         temp.fighter_b_link = matchup.fighter_b_link
#         temp.fighter_b_id = matchup.fighter_b_id
#         temp.weight_class = matchup.weight_class
#         temp.event_id = matchup.event_id
#         temp.rounds = matchup.rounds
#         temp.max_rounds = matchup.max_rounds
#         session.add(temp)
#     session.commit()
#     return {'status':'success'}

