from src.database_config.mongo_db import MongoDB
from src.modules.industrial_component_degradation.entities.register import Register

async def get_register_by_month_and_day_from_DB(month:str, day:str)->list[Register]:
    database = MongoDB()
    colection = database.client.industrial.component_degradation
    expression = "/{month}-{day}/i".format(month=str(month), day=str(day))
    try:
        # result = await colection.find({"title": "01-26T195109_081_mode3"}).to_list(None)
        result = await colection.find({"title": {"$regex":expression}}).to_list(None)

    except Exception as err:
        print(err)

    return result


async def get_register_file(file_name:str)->list[Register]:
    database = MongoDB()
    colection = database.client.industrial.component_degradation
    result = await colection.find({"title":file_name}).to_list(None)
    return result