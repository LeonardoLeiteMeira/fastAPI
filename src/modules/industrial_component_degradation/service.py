from modules.industrial_component_degradation.entities.register import Register
from modules.industrial_component_degradation.repository import get_register_by_month_and_day_from_DB, get_register_file

async def get_register_by_month_and_day(month:str, day:str)->list[Register]:
    #validate month and day
    register_list = await get_register_by_month_and_day_from_DB(month, day)
    return register_list

async def get_registers_by_file_name(file_name:str)->list[Register]:
    # validate name
    return await get_register_file(file_name)