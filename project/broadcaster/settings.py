from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nats_url: str
    webhook_url: str

    queue_group: str = "broadcaster"
    subject: str = "todo.events"
    is_debug: bool = False


settings = Settings()
