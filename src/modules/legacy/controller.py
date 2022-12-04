from fastapi import APIRouter
from modules.legacy.entities.processed_data import ProcessedData
from modules.legacy.service import get_processed_files, get_file_by_name, get_all_files

router = APIRouter(tags=["Legacy_data_source"])

@router.get("/legacy_files/file_names", response_model=list[str])
async def get_files_names():
    return await get_processed_files()

@router.get("/legacy_files/all", response_model=list[ProcessedData])
async def get_files():
    # return await get_processed_files()
    return await get_all_files()

@router.get("/legacy_files/{file_name}", response_model=list[ProcessedData])
async def get_file(file_name:str):
    return await get_file_by_name(file_name)