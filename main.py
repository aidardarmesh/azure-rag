from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_ai_foundry_endpoint: str = Field(alias="AZURE_AI_FOUNDRY_ENDPOINT")

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore"
    )


if __name__ == "__main__":
    settings = Settings()

    import pprint
    pprint.pprint(settings.model_dump())
