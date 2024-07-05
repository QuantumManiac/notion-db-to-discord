import requests
import os
from dataclasses import dataclass
from typing import Dict, Any, List, TypedDict

WEBHOOK_USERNAME = "Webhook"
WEBHOOK_AVATAR_URL = "https://i.imgur.com/4M34hi2.png"


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
    username: str = WEBHOOK_USERNAME
    avatar_url: str = WEBHOOK_AVATAR_URL

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
