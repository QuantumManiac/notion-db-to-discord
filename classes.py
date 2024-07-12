from typing import Dict, List, Tuple, TypedDict, NamedTuple, override
from dataclasses import dataclass
from datetime import datetime

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
    changed: Dict[str, Tuple[List[PropertyChange], datetime]]
    """Pages that had their properties changed in the diff. The key is the page id and the value is the list of 
    properties that were changed"""

    def is_empty(self) -> bool:
        return self.added == [] and self.removed == [] and self.changed == {}

    def merge_set(self, other_changed_set):
        """merges the changes from the other set into the current set
        """

        # For the added and removed pages, we simply add them to the new set if there is any
        self.added += other_changed_set.added
        self.removed += other_changed_set.removed
        
        # For each change we check if its already in our dict
        for page_id, (propertyList, timestamp) in other_changed_set.changed.items():
            if page_id in self.changed:
                property_changes, new_timestamp = self.changed[page_id]
                if timestamp > new_timestamp:
                    new_timestamp = timestamp
                
                self.changed[page_id] = (propertyList + property_changes, new_timestamp)
            else:
                self.changed[page_id] = (propertyList, timestamp)

