from typing import Dict, List, Tuple, TypedDict, NamedTuple
from dataclasses import dataclass

Property = NamedTuple("Property", [("name", str), ("value", str)])

class Page(TypedDict):
    """Represents a Notion page
    """
    page_id: str
    created_time: str
    last_edited_time: str
    properties: Dict[str, Property]
    url: str
    

class PropertyChange(TypedDict):
    """Represents a change in a property
    """
    property_name: str
    old_value: str
    new_value: str

@dataclass
class ChangeSet():
    """Represents a set of changes between two dictionaries
    """
    added: List[Page]
    """Pages that were added in the diff"""
    removed: List[Page]
    """Pages that were removed in the diff"""
    changed: List[Tuple[Page, List[PropertyChange]]]
    """Pages that had their properties changed in the diff. The key is the page id and the value is the list of 
    properties that were changed"""

    def is_empty(self) -> bool:
        return len(self.added) == 0 and len(self.removed) == 0 and len(self.changed) == 0
