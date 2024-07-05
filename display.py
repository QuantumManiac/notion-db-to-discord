from classes import ChangeSet, Page, PropertyChange
from enum import Enum
from typing import List, Dict, Tuple
from webhook import WebhookEmbed

class MessageColor(Enum):
    ADD = 0x44CC00
    REMOVE = 0xFF2A00
    CHANGE = 0xFFD000
    
def generate_changeset_messages(changeset: ChangeSet) -> List[WebhookEmbed]:
    # changed: List[Tuple[Page, List[PropertyChange]]]
    res = []
    res += generate_added_messages(changeset.added)
    res += generate_removed_messages(changeset.removed)
    res += generate_changed_messages(changeset.changed)
    return res
    
def generate_properties_text(page: Page) -> str:
    lines = [f"{property.name}: `{property.value}`" for property in page["properties"].values()]

    return "\n".join(lines)

def generate_changes_text(changes: List[PropertyChange]) -> str:
    lines = []

    for change in changes:
        old_change_text = f"`{change["old_value"]}`" if len(change["old_value"]) == 0 else "(None)"
        new_change_text = f"`{change["new_value"]}`" if len(change["new_value"]) == 0 else "(None)"
            
        lines.append(f"{change['property_name']}: {old_change_text} → {new_change_text}")

    return "\n".join(lines)

def generate_added_messages(additions: List[Page]) -> List[WebhookEmbed]: 
    res = []
    for addition in additions:
        message = WebhookEmbed(
            title=f"Task Added: {addition['properties']['title'].value}",
            url=addition["url"],
            description=generate_properties_text(addition),
            color=MessageColor.ADD.value
        )
        
        res.append(message)

    return res
        
def generate_removed_messages(removals: List[Page]) -> List[WebhookEmbed]:
    res = []
        
    for removal in removals:
        message = WebhookEmbed(
            title=f"Task Deleted: {removal['properties']['title'].value}",
            url = removal["url"],
            description = "",
            color=MessageColor.REMOVE.value
        )
        
        res.append(message)
        
    return res

def generate_changed_messages(pages: List[Tuple[Page, List[PropertyChange]]]) -> List[WebhookEmbed]:
    res = []

    for page, changes in pages:
        message = WebhookEmbed(
            title = f"Task Changed: {page['properties']['title'].value}",
            url = page["url"],
            description = generate_changes_text(changes),
            color = MessageColor.CHANGE.value
        )
        
        res.append(message)

    return res
