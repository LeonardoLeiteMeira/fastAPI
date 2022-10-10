from base_models.base_models import ModelName
from base_models.models import Person
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from modules.fast_api_tests import fast_api_tests_routers
from modules.personal_data.repository.repository import MongoConnection

app = FastAPI()

database = MongoConnection()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(fast_api_tests_routers)


@app.post("/person/create", response_model=Person)
async def create_person(person: Person, nameWithValidation: str | None = Query(default=None, max_length=5)):
    print("Name with validation in query: {}".format(nameWithValidation))
    print("Person Data:\nFull name: {name} ".format(name=person.name))
    origim: str = ""
    if person.city is not None:
        origim += person.city

    if person.country is not None:
        origim += " - " + person.country

    print("Origim: {}".format(origim))

    created_person = await database.createPerson(person)

    return created_person


@app.get("/people/getall", response_model=list[Person])
async def get_all_people():
    people = await database.getPeople()
    return people


@app.get("/testmongodb/names")
async def get_people_names():
    names = await database.getListOfNames()
    return names


@app.delete("/testmongodb/delete/")
async def delete_person(name: str | None = None, id: str | None = None):
    result: bool = False
    if id is not None:
        result = await database.deleteById(id)
        return return_delection(result)

    if name is None:
        raise HTTPException(status_code=400, detail="Id or Name is needed")

    result = await database.deleteByName(name)

    return return_delection(result)


@app.put("/testmongodb/update")
async def update_person(person: Person):
    result = await database.updatePersonById(person)
    if result is True:
        return {"result": "Person {} updated with success".format(str(person.id))}

    raise HTTPException(status_code=400, detail="Person not found")


@app.get("/testmongodb/getbyname/{name}", response_model=list[Person])
async def get_by_name(name: str):
    result = await database.findPerson(name)
    return result


def return_delection(result: bool):
    if result is True:
        return {"Status": "Deleted with success"}
    else:
        raise HTTPException(status_code=500, detail="Interno error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
