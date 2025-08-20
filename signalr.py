import json
import logging
from azure.messaging.webpubsubservice import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

#logging.basicConfig(level=logging.DEBUG)

class Settings(BaseSettings):
    signalr_endpoint: str = Field(alias="SIGNALR_ENDPOINT")
    signalr_hub_name: str = Field(alias="SIGNALR_HUB_NAME")
    signalr_access_key: str = Field(alias="SIGNALR_ACCESS_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

def send_signalr_message():
    try:
        # Load settings
        settings = Settings()
        print(f"Using SignalR endpoint: {settings.signalr_endpoint}")
        print(f"Using hub name: {settings.signalr_hub_name}")
        print(f"Using access key: {settings.signalr_access_key}")

        # Create the SignalR service client with the Azure SDK
        service_client = WebPubSubServiceClient(
            endpoint=settings.signalr_endpoint,
            hub=settings.signalr_hub_name,
            credential=AzureKeyCredential(settings.signalr_access_key)
        )
        
        # Message to send - properly formatted for SignalR
        message_content = {
            "target": "broadcastMessage",
            "arguments": [
                {
                    "text": "Hello from Azure SignalR!",
                    "sender": "user123",
                    "timestamp": "2025-08-20T14:56:00Z"
                }
            ]
        }

        
        # Send message to all connected clients
        service_client.send_to_all(
            message=message_content,
            content_type="application/json"
        )
        
        print("Message sent successfully!")
        
    except Exception as e:
        logging.error(f"Error sending SignalR message: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_signalr_message()
