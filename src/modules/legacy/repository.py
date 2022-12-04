from database_config.mongo_db import MongoDB


async def get_list_of_legacy_files_processed():
    database = MongoDB()
    collection = database.client.industrial.processed_data
    try:
        result = await collection.find({},{"file":1,"_id":0}).to_list(None)
        return result
    except Exception as err:
        print(err)

async def get_file_by_name(file_name:str):
    database = MongoDB()
    collection = database.client.industrial.processed_data
    try:
        result = await collection.find({"file":file_name}).to_list(None)
        return result
    except Exception as err:
        print(err)

async def get_all_files():
    database = MongoDB()
    collection = database.client.industrial.processed_data
    try:
        result = await collection.find().to_list(None)
        return result
    except Exception as err:
        print(err)