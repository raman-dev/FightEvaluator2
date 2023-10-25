from fastapi import FastAPI
from pydantic import BaseModel

# app = FastAPI()

"""
    fastapi implements openapi

    http operations/methods are
    
    post
    get
    put
    delete
    ...etc
    
    use @app.operation(args)
    as a decorator on a function to implement an http operation/method

    example

    @app.get('/img') -> the func() function returns the result
    of an http 'get' operation on the path '/img'
    async def func():
    
    async is not necessary to define functions
    async is only necessary if the function awaits on something 
    like a 3rd party library 
"""
# @app.get("/")
# async def root():
#     return {"message" : "Hello World"}

# @app.get("/example")
# async def example():
#     return {"message": "Example get path"}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id":item_id}
# can also make arguements typed
# @app.get("/items/{item_id}")
# async def read_item(item_id: int):
#     return {"item_id":item_id}

"""
    order matters paths are matched top down
# """
# @app.get("/users/about")
# async def about_user():
#     return {"userData":"data0"}

# @app.get("/users/{user_id}")
# async def read_user(user_id: str):
#     return {"user_id":user_id}

"""

    query parameters are key-value pairs after a ? in the path

"""
#this is a request model 
#when fastapi processes a request it can automatically fillout the model
#if the type is specified
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None



app = FastAPI()

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

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_first_name: str
    author_last_name: str
    title: str

#a list of 30 book titles and their authors
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


@app.post("/items/")
async def create_item(item: Item):
    return item

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

