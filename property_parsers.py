from typing import Dict, Any
from classes import Property

def parse_created_by(data: Dict[str, Any]) -> str:
    """Parses the created by property of a Notion

    Args:
        data: The data of the created by property

    Returns:
        The name of the person who created the Notion page
    """    
    return data["created_by"]["name"]

def parse_people(data: Dict[str, Any]) -> str:
    """Parses the people property of a Notion page

    Args:
        data: The data of the people property

    Returns:
        A string containing the names of the people in the people property, separated by commas
    """    
    people_names = [person["name"] for person in data["people"]]
    
    res = ", ".join(people_names)
    return res

def parse_rich_text(data: Dict[str, Any]) -> str:
    """Parses the rich text property of a Notion page

    Args:
        data: The data of the rich text property

    Returns:
        A string containing the rich text in plain text format
    """    
    res = ""
    for item in data["rich_text"]:
        res += item["plain_text"]
    return res

def parse_select(data: Dict[str, Any]) -> str:
    """Parses the select property of a Notion page

    Args:
        data: The data of the select property

    Returns:
        The name of the selected item in the select property
    """    
    if data["select"] is None:
        return "(None)"
    
    return data["select"]["name"]

def parse_status(data: Dict[str, Any]) -> str:
    """Parses the status property of a Notion page

    Args:
        data: The data of the status property

    Returns:
        The name of the status in the status property
    """    
    status = data["status"]["name"]
    return status

def parse_title(data: Dict[str, Any]) -> str:
    """Parses the title property of a Notion page

    Args:
        data: The data of the title property

    Returns:
        A string containing the title in plaintext format
    """
    if len(data["title"]) == 0:
        return "(Untitled)"

    res = ""
    for item in data["title"]:
        res += item["plain_text"]
    return res

DATA_TYPE_PARSER_MAPPING = {
    "created_by": parse_created_by,
    "people": parse_people,
    "rich_text": parse_rich_text,
    "select": parse_select,
    "status": parse_status,
    "title": parse_title
}

def parse_properties(data: Dict[str, Any]) -> Dict[str, Property]:
    """Parses the properties of a Notion page

    Args:
        data: The data of the properties of a Notion page

    Returns:
        A dictionary containing the parsed properties of the Notion page, where each key is the property id
    """
    res = {}

    for key, value in data.items():
        property_id = value["id"]
        parser = DATA_TYPE_PARSER_MAPPING.get(value["type"])

        if parser is None: # Skip unsupported properties
            continue
        
        res[property_id] = Property(key, parser(value)) 
    
    return res
        
        
