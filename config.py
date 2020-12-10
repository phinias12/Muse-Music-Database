import os
from dotenv import load_dotenv

load_dotenv('.env')

SECRET_KEY=os.getenv('SECRET_KEY')
DB_HOST=os.getenv('DB_HOST')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_NAME=os.getenv('DB_NAME')
API_KEY=os.getenv('API_KEY')