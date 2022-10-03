from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, Field

class ModelName(str, Enum):
    leo = "Leo"
    alice = "Alice"
    cicero = "Cicero"
    artur = "Artur"
    laura = "Laura"

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Person(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name:str = Field(...)
    lastname:str = Field(...)
    country: str | None = Field(...)
    city: str | None = Field(None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}