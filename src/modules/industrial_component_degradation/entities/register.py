from bson import ObjectId
from pydantic import BaseModel, Field
from src.base_models.base_models import PyObjectId

class Register(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title:str = Field(...)
    timestamp:float = Field(...)
    pCut_Motor_Torque:float = Field(...)
    pCut_CTRL_Position_controller_Lag_error:float = Field(...)
    pCut_CTRL_Position_controller_Actual_position:float = Field(...)
    pCut_CTRL_Position_controller_Actual_speed:float = Field(...)
    pSvolFilm_CTRL_Position_controller_Actual_position:float = Field(...)
    pSvolFilm_CTRL_Position_controller_Actual_speed:float = Field(...)
    pSvolFilm_CTRL_Position_controller_Lag_error:float = Field(...)
    pSpintor_VAX_speed:float = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}