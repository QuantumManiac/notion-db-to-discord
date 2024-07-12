from typing import Dict, List, Tuple, TypedDict, NamedTuple, override
from dataclasses import dataclass
from datetime import time, datetime

Property = NamedTuple("Property", [("name", str), ("value", str)])

@dataclass
class Page():
    """Represents a Notion page
    """
    page_id: str
    created_time: str
    last_edited_time: str
    properties: Dict[str, Property]
    url: str
    
    @override
    def __hash__(self) -> int:
        return hash(self.page_id)
     

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
    changed: Dict[Page, Tuple[List[PropertyChange], datetime]]
    """Pages that had their properties changed in the diff. The key is the page id and the value is the list of 
    properties that were changed"""

    def is_empty(self) -> bool:
        return len(self.added) == 0 and len(self.removed) == 0 and len(self.changed) == 0

    def merge_set(self, other_changed_set: ChangeSet):
        """merges the changes from the other set into the current set
        """

        # For the added and removed pages, we simply add them to the new set if there is any
        self.added += other_changed_set.added
        self.removed += other_changed_set.removed
        
        # For each change we check if its already in our dict
        for page, (propertyList, timestamp) in other_changed_set.changed.items():
            if page in self.changed:
                property_changes, new_timestamp = self.changed[page]
                if timestamp > new_timestamp:
                    new_timestamp = timestamp
                
                self.changed[page] = (propertyList + property_changes, new_timestamp)
            else:
                self.changed[page] = (propertyList, timestamp)

