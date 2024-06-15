import dataclasses

from server.config import app_config


@dataclasses.dataclass
class DbConfig:
    host: str = app_config.db_host
    port: str = app_config.db_port
    user: str = app_config.db_user
    password: str = app_config.db_password
    name: str = app_config.db_name

    def db_url(self):
        # NOTE: I assume we always use same kind of database for a server here
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @classmethod
    def from_json(cls, json: dict):
        field_names = {field.name for field in dataclasses.fields(cls)}
        kwargs = {
            key: value
            for key, value in json.items()
            if key in field_names and value is not None
        }
        return cls(**kwargs)
