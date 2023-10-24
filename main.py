from typing import Optional,List
from sqlmodel import Field, Session, SQLModel, create_engine, select

from fastapi import FastAPI
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_first_name: str
    author_last_name: str
    title: str

sqlite_file_name ="sqlmodel_test.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url,echo=True, connect_args=connect_args)

app = FastAPI()
#a list of 30 book titles and their authors
book_titles_and_authors = [
    ("Harry Potter and the Philosopher's Stone", "J. K. Rowling"),
    ("Harry Potter and the Chamber of Secrets", "J. K. Rowling"),
    ("Harry Potter and the Prisoner of Azkaban", "J. K. Rowling"),
    ("Harry Potter and the Goblet of Fire", "J. K. Rowling"),
    ("Harry Potter and the Order of the Phoenix", "J. K. Rowling"),
    ("Harry Potter and the Half-Blood Prince", "J. K. Rowling"),
    ("Harry Potter and the Deathly Hallows", "J. K. Rowling"),
    ("The Hobbit", "J. R. R. Tolkien"),
    ("The Fellowship of the Ring", "J. R. R. Tolkien"),
    ("The Two Towers", "J. R. R. Tolkien"),
    ("The Return of the King", "J. R. R. Tolkien"),
    ("1984", "George Orwell"),
    ("Animal Farm", "George Orwell"),
    ("Brave New World", "Aldous Huxley"),
    ("Fahrenheit 451", "Ray Bradbury"),
    ("Foundation", "Isaac Asimov"),
    ("Dune", "Frank Herbert"),
    ("Nineteen Eighty-Four", "George Orwell"),
    ("The Moon Is a Harsh Mistress", "Robert A. Heinlein"),
    ("Stranger in a Strange Land", "Robert A. Heinlein"),
    ("The Diamond Age", "Neal Stephenson"),
    ("Snow Crash", "Neal Stephenson"),
    ("American Gods", "Neil Gaiman"),
    ("Coraline", "Neil Gaiman"),
    ("Stardust", "Neil Gaiman"),
    ("Neverwhere", "Neil Gaiman"),
    ("The Graveyard Book", "Neil Gaiman"),
    ("Good Omens", "Neil Gaiman"),
    ("The Ocean at the End of the Lane", "Neil Gaiman"),
    ("The Left Hand of Darkness", "Ursula K. Le Guin"),
    ("The Dispossessed", "Ursula K. Le Guin"),
]

def create_sample_data():
    #create 25 sample books
    with Session(engine) as session:
        for i in range(0,25):
            book = Book(
                id=i+1,
                author_first_name=" ".join(book_titles_and_authors[i][1].split(" ")[:-1]),
                author_last_name=book_titles_and_authors[i][1].split(" ")[-1],
                title=book_titles_and_authors[i][0],
            )
            session.add(book)
        session.commit()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app.mount("/static", StaticFiles(directory=Path("static")), name="static")
# templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_start():
    create_db_and_tables()
    # create_sample_data()

@app.post("/books/")
def create_book(book: Book):
    with Session(engine) as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

@app.get("/books/", response_model=List[Book])
def read_books():
    with Session(engine) as session:
        books = session.exec(select(Book)).all()
        return books

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
