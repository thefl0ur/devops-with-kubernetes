from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_address: str = "0.0.0.0"
    server_port: int = 8001

    backend_address: str

    image_ttl: int = 60 * 60
    image_cache_folder: str
    image_name: str = "image.png"

    templates_dir: str = "todo_app/templates"
    random_image_source: str = "https://picsum.photos/500"


settings = Settings()
