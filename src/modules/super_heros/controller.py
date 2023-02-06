from fastapi import APIRouter

from src.modules.super_heros.models.hero import Hero
from src.modules.super_heros.repository import create_hero, read_heros, update_hero, delete_hero


router = APIRouter(tags=["Super Heros"])

@router.post("/create")
async def create_hero_controller(hero: Hero):
    result = await create_hero(hero)
    if result.isSuccess:
        return 201
    return 400

@router.get("/read", response_model=list[Hero])
async def read_hero_controller():
    result =  await read_heros()
    if result.isSuccess:
        return result.data
    return 400

@router.patch("/update")
async def update_hero_controller(updated_hero: Hero):
    result = await update_hero(updated_hero)
    if result.isSuccess:
        return 201
    return 400

@router.delete("/delete/{id}")
async def delete_hero_controller(id:str):
    await delete_hero(id)
    return 202