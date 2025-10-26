from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_address: str = "0.0.0.0"
    server_port: int = 8001

    db_connections_string: str


settings = Settings()
