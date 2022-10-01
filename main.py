from models import ModelName, Person
from fastapi import FastAPI, Query
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Access /docs to see the documentation"}


@app.get("/items/{id}")
async def items(id:int):
    return {
        "phone":{
            "id":id,
            "name":"iPhone 12",
            "memory":128,
            "user":"Leonardo Leite",
        },
    }


@app.get("/models_description/{model_name}")
async def getModel(model_name:ModelName):
    if model_name is ModelName.artur or model_name is ModelName.laura:
        return {"response":"Brothers"}

    if model_name is ModelName.alice or model_name is ModelName.cicero:
        return {"response":"Parents"}

    if model_name is ModelName.leo:
        return {"response":"It's me"}

@app.get("/models")
async def getModels(mySelf:bool, brothers:bool|None = True):
    response:dict = {}
    response["Parents"] = {"Mother":ModelName.alice.value, "Father":ModelName.cicero.value}

    if mySelf is True:
        response["Me"] = ModelName.leo
    
    if brothers is True:
        response["Brothers"] = {"Sister":ModelName.laura.value, "Brother":ModelName.artur.value}

    return response


@app.post("/person/create")
async def createPerson(person:Person, nameWithValidation:str|None = Query(default=None, max_length=5)):
    print("Name with validation in query: {}".format(nameWithValidation))
    print("Person Data:\nFull name: {name} ".format(name=person.name))
    origim:str = ""
    if person.city is not None:
        origim += person.city
    
    if person.country is not None:
        origim += " - " + person.country

    print("Origim: {}".format(origim))

    return {"message": "Created with success!"}



if __name__ == "__main__":
    uvicorn.run(app,host="0.0.0.0",port=8000)