from fastapi import APIRouter

from src.modules.super_heros.models.hero import Hero
from src.modules.super_heros.repository import create_hero, read_heros, update_hero, delete_hero


router = APIRouter(tags=["Super Heros"])

@router.post("/create")
async def create_hero_controller(hero: Hero):
    await create_hero(hero)
    return 201

@router.get("/read", response_model=list[Hero])
async def read_hero_controller():
    heros =  await read_heros()
    return heros

@router.patch("/update")
async def update_hero_controller(updated_hero: Hero):
    await update_hero(updated_hero)
    return 201

@router.delete("/delete/{id}")
async def delete_hero_controller(id:str):
    await delete_hero(id)
    return 202