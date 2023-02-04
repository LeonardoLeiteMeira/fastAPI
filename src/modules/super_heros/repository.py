from src.config.database_config.mongo_db import MongoDB
from src.modules.super_heros.models.hero import Hero
from fastapi.encoders import jsonable_encoder

def _get_heros_collections():
    database = MongoDB()
    collection = database.client.super_heros.heros
    return collection

async def create_hero(hero:Hero):
    collection = _get_heros_collections()
    try:
        hero_json = jsonable_encoder(hero)
        result = await collection.insert_one(hero_json)
        print(result)
    except Exception as e:
        print(e)

async def read_heros():
    collection = _get_heros_collections()
    try:
        result = await collection.find().to_list(None)
        return result
    except Exception as e:
        print(e)

async def update_hero(updated_hero:Hero):
    collection = _get_heros_collections()
    try:
        id = str(updated_hero.id)
        hero_dict = updated_hero.__dict__
        hero_dict.pop("id", None)
        result = await collection.update_one({'_id': id}, {'$set': hero_dict})
        return result
    except Exception as e:
        print(e)

async def delete_hero(id:str):
    collection = _get_heros_collections()
    try:
        result = await collection.delete_one({"_id":id})
        return result
    except Exception as e:
        print(e)