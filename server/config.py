from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_schema: str
    db_url: str


app_config = Settings()
