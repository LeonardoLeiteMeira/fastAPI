from enum import Enum
from pydantic import BaseModel

class ModelName(str, Enum):
    leo = "Leo"
    alice = "Alice"
    cicero = "Cicero"
    artur = "Artur"
    laura = "Laura"


class Person(BaseModel):
    name:str
    lastName:str
    country: str|None = None
    city: str|None = None