from fastapi import APIRouter
from src.modules.industrial_component_degradation.entities.register import Register
from src.modules.industrial_component_degradation.service import get_register_by_month_and_day, get_registers_by_file_name

router = APIRouter(tags=["industrial_component_degradation"])

@router.get("/getIndustrialComponentsInfo/", response_model=list[Register])
async def get_info(month:str, day:str):
    result = await get_register_by_month_and_day(month, day)
    return result

@router.get("/getIndustrialComponentFile/",response_model=list[Register])
async def get_info_by_file_name(file_name:str):
    return await  get_registers_by_file_name(file_name)