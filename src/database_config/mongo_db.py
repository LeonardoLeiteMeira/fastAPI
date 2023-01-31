from src.base_models.singleton import Singleton
import motor.motor_tornado
from fastapi.encoders import jsonable_encoder


class MongoDB(metaclass=Singleton):
    def __init__(self):
        print("init class")
        self.client = motor.motor_tornado.MotorClient('localhost', 27017)