from pony.orm import *
from random import randint

db = Database()

#pony automatically generates primary key of type int if not specified
class Person(db.Entity):
    name = Required(str)
    age = Required(int)
    cars = Set('Car')

class Car(db.Entity):
    make = Required(str)
    model = Required(str)
    owner = Required(Person) #relation to Person object

# @db_session
# def createTable():
#     #bind to sqlite database with filename testdb.sqlite or create if not exists
#     db.bind(provider='sqlite', filename='testdb.sqlite', create_db=True)
#     #create the mapping of from class objects to database tables
#     db.generate_mapping(create_tables=True)#can safely have this always
#     #keyword arg create_tables=True will create tables if they don't exist
    

@db_session
def createObjects():
    names = ['John', 'Mary', 'Bob', 'Alice']
    makeModels = {'Ford': ['Fiesta', 'Focus', 'Mustang'], 'Honda': ['Civic', 'Accord', 'Jazz']}
    for name in names:
        p  = Person(name=name, age=randint(18, 35))
        makeIndex = randint(0, len(makeModels)-1)
        make = list(makeModels.keys())[makeIndex]
        model = makeModels[make][randint(0, len(makeModels[make])-1)]
        c = Car(make=make, model=model, owner=p)
    #all database operations need to be dont in a function with a 
    #db_session decorator 

# createTable()
# createObjects()
db.bind(provider='sqlite', filename='testdb.sqlite', create_db=True)
# @db_session
# def show():
#     print(Person.)
