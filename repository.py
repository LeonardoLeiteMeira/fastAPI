from hashlib import new
import motor.motor_tornado
from fastapi.encoders import jsonable_encoder

from models import Person

class MongoConnection:
    def __init__(self):
        self.client = motor.motor_tornado.MotorClient('localhost', 27017)
        #self.client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

        self.dbPessoas = self.client.pessoasData

    async def findPerson(self,name:str):
        document = await self.dbPessoas.pessoas.find({"name":name}).to_list(None)
        return document

    async def findPersonbyId(self,id:str):
        document = await self.dbPessoas.pessoas.find_one({"_id":id})
        return document

    async def getListOfNames(self):
        people = await self.dbPessoas.pessoas.find().to_list(None)
        names:list[str] = []
        for person in people:
            names.append((person["name"]))

        return names

    async def createPerson(self, person:Person):
        person_json = jsonable_encoder(person)
        new_person_info = await self.dbPessoas.pessoas.insert_one(person_json)
        new_person = await self.findPersonbyId(new_person_info.inserted_id)
        return new_person

    async def deleteByName(self, name:str):
        result = await self.dbPessoas.pessoas.delete_one({"name":name})
        if result.deleted_count == 1:
            return True
        
        return False

    async def deleteById(self, id:str):
        result = await self.dbPessoas.pessoas.delete_one({"_id":id})
        if result.deleted_count == 1:
            return True
        
        return False

    async def updatePersonById(self, person:Person):
        id = str(person.id)
        # verify this loop
        person = {k: attribute for k, attribute in person.dict().items() if attribute is not None}
        result = await self.dbPessoas.pessoas.update_one({"_id":id}, {"$set":person})
        if result.modified_count == 1:
            return True
        return False


 
