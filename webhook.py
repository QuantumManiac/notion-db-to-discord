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

"""
{
        "username": "Webhook",
        "avatar_url": "https://i.imgur.com/4M34hi2.png",
        "content": "Text message. Up to 2000 characters.",
        "embeds": [
            {
            "author": {
                "name": "Birdie♫",
                "url": "https://www.reddit.com/r/cats/",
                "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
            },
            "title": "Title",
            "url": "https://google.com/",
            "description": "Text message. You can use Markdown here. *Italic* **bold** __underline__ ~~strikeout~~ [hyperlink](https://google.com) `code`",
            "color": 15258703,
            "fields": [
                {
                "name": "Text",
                "value": "More text",
                "inline": True
                },
                {
                "name": "Even more text",
                "value": "Yup",
                "inline": True
                },
                {
                "name": "Use `\"inline\": true` parameter, if you want to display fields in the same line.",
                "value": "okay..."
                },
                {
                "name": "Thanks!",
                "value": "You're welcome :wink:"
                }
            ],
            "thumbnail": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Generic_Camera_Icon.svg/1024px-Generic_Camera_Icon.svg.png"
            },
            "image": {
                "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/WLE_Austria_Logo.svg/800px-WLE_Austria_Logo.svg.png"
            },
            "footer": {
                "text": "Woah! So cool! :smirk:",
                "icon_url": "https://i.imgur.com/fKL31aD.jpg"
            }
            }
        ]
    }
"""
