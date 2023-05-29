import os
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr


load_dotenv()


class SecretSettings(BaseSettings):
    secret_key: SecretStr = os.getenv('SECRET_KEY', 'asdf1234asdf')