import os
from dotenv import dotenv_values

config = dotenv_values(".env") 

DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_URL = os.getenv('DATABASE_URL')

