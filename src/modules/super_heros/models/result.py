from pydantic.generics import GenericModel
from typing import TypeVar, Generic

T = TypeVar("T")

class Result(GenericModel, Generic[T]):
    data: T | None
    isSuccess: bool
    error: Exception | None

    class Config:
        arbitrary_types_allowed = True