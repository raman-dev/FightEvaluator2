from typing import Optional,List
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

sqlite_file_name ="database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,echo=True, connect_args=connect_args)

app = FastAPI()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
# templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_start():
    create_db_and_tables()
    # create_sample_data()

@app.get("/")
async def index():
    return FileResponse("static/index.html")

@app.get("/assessment")
async def index():
    return FileResponse("static/assessment.html")

@app.get("/matchup")
async def index():
    return FileResponse("static/matchup.html")

@app.get("/styles.css")
async def styles():
    return FileResponse("static/styles/styles.css")

@app.get("/static/media/{resource_name}")
async def media(resource_name):
    return FileResponse("static/media/"+resource_name)
