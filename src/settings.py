from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    step_queue_url: str = ""


settings = Settings()
