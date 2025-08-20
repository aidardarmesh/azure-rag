import requests
import json
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    signalr_endpoint: str = Field(alias="SIGNALR_ENDPOINT")
    signalr_hub_name: str = Field(alias="SIGNALR_HUB_NAME")
    signalr_access_key: str = Field(alias="SIGNALR_ACCESS_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

# Construct the URL for send message
url = f"{settings.signalr_endpoint}/api/v1/hubs/{settings.signalr_hub_name}/:send?api-version=2023-05-01"

# Your static JSON message to broadcast
message = {
    "target": "broadcastMessage",  # The method clients listen to
    "arguments": [
        {
            "text": "Hello from Python broadcast!",
            "otherKey": "otherValue"
        }
    ]
}

# Headers required for request
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {settings.signalr_access_key}"
}

# Send POST request to broadcast the message
response = requests.post(url, headers=headers, data=json.dumps(message))

# Print response status
print("Status Code:", response.status_code)
print("Response Body:", response.text)
