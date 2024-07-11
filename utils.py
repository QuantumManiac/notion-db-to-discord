from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Literal
from classes import Page, ChangeSet, PropertyChange, Property
from property_parsers import parse_properties
from dictdiffer import diff
from collections import defaultdict

def parse_db_query_response(data: Dict[str, Any]) -> Dict[str, Page]:
    """Parses the response of a database query from Notion into a dictionary of page objects, 
    where the key is the page_id

    Args:
        data: The response of a database query from Notion

    Returns:
        A dictionary containing the parsed pages, where each key is the Page's page_id
    """    
    res = {}
    for page in data["results"]:
        parsed_page = parse_page_data(page)
        res[parsed_page["page_id"]] = parsed_page

    return res
        
def parse_page_data(page_data: Dict[str, Any]) -> Page:
    """Parses a Notion page into a Page object

    Args:
        page_data: The data of the Notion page

    Returns:
        A Page object containing the parsed data of the Notion page
    """    
    properties = page_data["properties"]
    
    res = Page(
        page_id=page_data["id"],
        created_time=page_data["created_time"],
        last_edited_time=page_data["last_edited_time"],
        properties=parse_properties(properties),
        url=page_data["url"]
    )
    
    return res

def identify_changes(old_data: Dict[str, Page], new_data: Dict[str, Page]) -> ChangeSet:
    """Identifies the changes between two sets of Notion pages

    Args:
        old_data: The old set of pages
        new_data: The new set of pages

    Returns:
        The changes between the two sets of pages
    """
    delta_list = diff(old_data, new_data)
    changeset = parse_diff(new_data, delta_list)
    return changeset


def generate_id_title_mapping(data: Dict[str, Page]) -> Dict[str, str]:
    """Creates a dictionary that maps the page_id to the page title
    Args:
        data: The data of the Notion pages, represented as a dictionary where the key is the page_id

    Returns:
        A dictionary where the key is the page_id and the value is the page title

    """
    res = {}
    for page_id, page in data.items():
        res[page_id] = page["properties"]["title"]
    return res

def generate_id_title_mappings(old_data: Dict[str, Page], new_data: Dict[str, Page]) -> Dict[str, str]:
    """Generates an page_id to title mapping for the old and new page data. Titles in the new data will overwrite 
    titles in the old data

    Args:
        old_data: The old page data
        new_data: The new page data

    Returns:
        The generated page_id to title mapping
    """
    old_mapping = generate_id_title_mapping(old_data)
    new_mapping = generate_id_title_mapping(new_data)

    combined_mappings = old_mapping | new_mapping
    return combined_mappings
    
def parse_diff(data: Dict[str, Page], diff: List[Tuple]) -> ChangeSet:   
    """Parses a generated diff into a ChangeSet

    Args:
        diff: The diff to parse

    Returns:
        The resulting ChangeSet
    """
    res = ChangeSet(
        added=[],
        removed=[],
        changed={}
    ) 

    # List[Tuple[Page, List[PropertyChange]]] 
    # Dict[Page, Tuple[List[PropertyChange], datetime]]
    changes: Dict[str, List[PropertyChange]] = defaultdict(list) # A dictionary that maps the page_id to the list of changes

    change_type: Literal["add", "remove", "change"]
    change_key: str
    for change_type, change_key, change_value in diff:
        if change_type == 'add' and change_key == '': # Additions are only considering added pages
            res.added = parse_add_or_remove(change_value)
        elif change_type == 'remove' and change_key == '': # Removals are only considering removed pages
            res.removed = parse_add_or_remove(change_value) 
        elif change_type == 'change':
            change_key_tokens = change_key.split('.')
            
            timestamp = datetime.now()
            # I should be parsing the time here, but I will leave it till tonight to figure that out
            if len(change_key_tokens) <= 2: # We are only interested in changes to properties, not the page itself
                #timestamp = datetime.fromisoformat(change_key_tokens[1])
                continue

            page_id, _, _ = change_key_tokens
            change = parse_change(change_value)

            changes[page_id].append(change)

            for page_id, change_list in changes.items():
                res.changed[data[page_id]] = (change_list, timestamp)

    return res

def parse_add_or_remove(delta: List[Tuple[str, Page]]) -> List[Page]:
    """Parse the added or removed pages from a diff

    Args:
        delta: The diff to parse

    Returns:
        The list of added or removed pages
    """    
    res = []
    for _, page in delta:
        res.append(page)
        
    return res

def parse_change(delta: Tuple[Property, Property]) -> PropertyChange:
    """Parses a change in a property from a diff

    Args:
        delta: The diff to parse

    Returns:
        The resulting PropertyChange
    """    
    old, new = delta

    property_name: str = new.name

    res = PropertyChange(
        property_name=property_name,
        old_value=old.value,
        new_value=new.value
    )

    return res
