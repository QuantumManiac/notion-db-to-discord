import requests
import os
from dataclasses import dataclass
from typing import Dict, Any, List, TypedDict

@dataclass
class WebhookEmbed():
    """Represents an embed in a Discord webhook message
    """
    title: str
    url: str
    description: str
    color: int

    def to_json(self) -> Dict[str, Any]:
        json = {  
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "color": self.color
        }

        return json

@dataclass
class WebhookMessage():
    """Represents a Discord webhook message
    """
    embeds: List[WebhookEmbed]
    username: str = os.environ.get("WEBHOOK_USERNAME", "Webhook")
    avatar_url: str = os.environ.get("WEBHOOK_AVATAR_URL", "")

    def to_json(self) -> Dict[str, Any]:
        json = {
            "username": self.username,
            "avatar_url": self.avatar_url,
            "embeds": [embed.to_json() for embed in self.embeds]
        }

        return json

def generate_message(embeds: List[WebhookEmbed]) -> WebhookMessage:
    message = WebhookMessage(
        embeds=embeds
    )

    return message

def send_message(message: WebhookMessage):    
    result = requests.post(os.environ["DISCORD_WEBHOOK_URL"], json=message.to_json())
    return result
