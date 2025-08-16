from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_ai_foundry_endpoint: str = Field("AZURE_AI_FOUNDRY_ENDPOINT")


if __name__ == "__main__":
    settings = Settings()

    import pprint
    pprint.pprint(settings.model_dump())
