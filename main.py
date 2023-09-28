from fastapi import FastAPI

app = FastAPI()

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
@app.get("/")
async def root():
    return {"message" : "Hello World"}

@app.get("/example")
async def example():
    return {"message": "Example get path"}

# @app.get("/items/{item_id}")
# async def read_item(item_id):
#     return {"item_id":item_id}
# can also make arguements typed
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id":item_id}

"""
    order matters paths are matched top down
"""
@app.get("/users/about")
async def about_user():
    return {"userData":"data0"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id":user_id}

"""

    query parameters are key-value pairs after a ? in the path

"""


