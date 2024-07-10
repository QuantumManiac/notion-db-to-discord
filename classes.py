from typing import Dict, List, Tuple, TypedDict, NamedTuple
from dataclasses import dataclass
from datetime import time, datetime

Property = NamedTuple("Property", [("name", str), ("value", str)])

class Page(TypedDict):
    """Represents a Notion page
    """
    page_id: str
    created_time: str
    last_edited_time: str
    properties: Dict[str, Property]
    url: str
    

    def eq(self, other):
        """Compares page_id
        """
        return self.page_id == other.page_id

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
    changed: List[Tuple[Page, List[PropertyChange], datetime]]
    """Pages that had their properties changed in the diff. The key is the page id and the value is the list of 
    properties that were changed"""

    def is_empty(self) -> bool:
        return len(self.added) == 0 and len(self.removed) == 0 and len(self.changed) == 0

    def merge_set(self, other_changed_set):
        """merges the changes from the other set into the current set
        """

        # For the added and removed pages, we simply add them to the new set if there is any
        self.added += other_changed_set.added
        self.removed += other_changed_set.removed
        

        # We compare if there are any changes in the same page and coalece
        # Horribly underoptimized, we will get back to this later
        for other_page, other_property_change_list, other_time in other_changed_set.changed:
            for page, property_change_list, timestamp in self.changed:
                if page == other_page:
                    property_change_list += other_property_change_list
                    # We should be able to assume that other_time > time
                    if other_time > timestamp:
                        timestamp = other_time
