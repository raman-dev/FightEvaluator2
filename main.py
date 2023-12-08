from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# from models import *
from routers import fightevents,assessments,matchups,fighters,notes,temp

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path("static")), name="static")
app.include_router(fightevents.router)
app.include_router(assessments.router)
app.include_router(matchups.router)
app.include_router(fighters.router)
app.include_router(notes.router)
# app.include_router(temp.router)