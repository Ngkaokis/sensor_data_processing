from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_schema: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    broker_url: str
    log_level: Optional[str] = None
    log_file: Optional[str] = None


app_config = Settings()
