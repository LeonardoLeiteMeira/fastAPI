from bson import ObjectId
from pydantic import BaseModel, Field

from src.base_models.base_models import PyObjectId


class Hero(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    real_name:str = Field(...)
    nickname:str = Field(...)
    description:str = Field(...)

    class Config:
        #Quando definida como True, permite que o Pydantic atribua valores aos campos de modelo baseados nos nomes dos campos, em vez de nos nomes dos argumentos na chamada da função.
        #pode instanciar um objeto do modelo Hero passando valores como um dicionário, onde as chaves do dicionário correspondem aos nomes dos campos do modelo:
        allow_population_by_field_name = True

        # permite que tipos de dados não especificados no modelo sejam incluídos nos dados de entrada.
        arbitrary_types_allowed = False

        #define como certos tipos de dados serão codificados em formato JSON. No caso deste exemplo, o tipo ObjectId será codificado como uma string.
        #PyObjectId extende de ObjectId
        json_encoders = {ObjectId: str}
