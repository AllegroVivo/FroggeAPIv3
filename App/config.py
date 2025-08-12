from pydantic_settings import BaseSettings
from dotenv import load_dotenv
################################################################################
class Settings(BaseSettings):

    DEVELOPMENT_DATABASE_URL: str
    PRODUCTION_DATABASE_URL: str

    DEBUG: bool = False

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_MINUTES: int

    FROGGE_REGISTRATION_PASSWORD: str

################################################################################

load_dotenv()
# noinspection PyArgumentList
settings = Settings()

################################################################################
