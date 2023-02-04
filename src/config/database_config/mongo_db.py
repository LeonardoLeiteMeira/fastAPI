from src.config.env_config import DATABASE_URL, DATABASE_PORT
from src.base_models.singleton import Singleton
import motor.motor_tornado
from fastapi.encoders import jsonable_encoder


class MongoDB(metaclass=Singleton):
    def __init__(self):
        port = int(DATABASE_PORT)
        url = DATABASE_URL
        self.client = motor.motor_tornado.MotorClient(url, port)