from dotenv import load_dotenv
from notion_client import Client
from typing import Dict
from classes import Page
from webhook import generate_message, send_message
from display import generate_changeset_messages
import os
from utils import parse_db_query_response, identify_changes
from time import sleep
import logging
import sys

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])


def get_database_data() -> Dict:
    db = notion.databases.query(database_id=os.environ["NOTION_DATABASE_ID"])
    return db # type: ignore

def get_state() -> Dict[str, Page]:
    db_data = get_database_data()
    return parse_db_query_response(db_data)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger()
    prev_state = []
    prev_state = get_state()

    while True:
        new_state = get_state()
        changeset = identify_changes(prev_state, new_state)

        if changeset.is_empty():
            logger.info("No changes detected")
        else:
            messages = generate_changeset_messages(changeset)
            logger.info(f"Changes detected. {len(messages)} to be sent.")
            message = generate_message(messages)
            send_message(message)
            prev_state = new_state

        sleep(60)

if __name__ == "__main__":
    main()


"""
{
    "added": [
        {
            "page_id": "f88027cf-0326-489c-8348-ca04c92a9896",
            "created_time": "2024-07-05T01:28:00.000Z",
            "last_edited_time": "2024-07-05T01:28:00.000Z",
            "properties": {
                "QTri": Property(name="Description", value=""),
                "VlyJ": Property(name="Created by", value="Chamath Wijesekera"),
                "b%7CS%40": Property(name="Status", value="In progress"),
                "gQ%7Di": Property(name="Assignee", value=""),
                "i%60cU": Property(name="Priority", value="Low Priority"),
                "lm%5Cx": Property(name="Project", value="(None)"),
                "title": Property(name="Name", value="Temp Page"),
            },
            "url": "https://www.notion.so/Temp-Page-f88027cf0326489c8348ca04c92a9896",
        }
    ],
    "removed": [
        {
            "page_id": "c56a4ce5-b0b7-4511-9025-4dbd5a843ed2",
            "created_time": "2024-06-25T21:36:00.000Z",
            "last_edited_time": "2024-06-25T21:36:00.000Z",
            "properties": {
                "QTri": Property(
                    name="Description",
                    value="Look into better ore processing using new technologies",
                ),
                "VlyJ": Property(name="Created by", value="Chamath Wijesekera"),
                "b%7CS%40": Property(name="Status", value="To-do"),
                "gQ%7Di": Property(name="Assignee", value=""),
                "i%60cU": Property(name="Priority", value="Low Priority"),
                "lm%5Cx": Property(name="Project", value="(None)"),
                "title": Property(name="Name", value="Improved ore processing"),
            },
            "url": "https://www.notion.so/Improved-ore-processing-c56a4ce5b0b7451190254dbd5a843ed2",
        }
    ],
    "changed": [
        (
            {
                "page_id": "0ce0855a-4395-46a4-b0a4-b1e467f27d64",
                "created_time": "2024-06-26T01:51:00.000Z",
                "last_edited_time": "2024-07-05T01:28:00.000Z",
                "properties": {
                    "QTri": Property(name="Description", value="Test 2"),
                    "VlyJ": Property(name="Created by", value="Robert Cai"),
                    "b%7CS%40": Property(name="Status", value="Blocked"),
                    "gQ%7Di": Property(name="Assignee", value="Robert Cai"),
                    "i%60cU": Property(name="Priority", value="Low Priority"),
                    "lm%5Cx": Property(name="Project", value="(None)"),
                    "title": Property(name="Name", value="Ramen Shop"),
                },
                "url": "https://www.notion.so/Ramen-Shop-0ce0855a439546a4b0a4b1e467f27d64",
            },
            [
                {
                    "property_name": "Description",
                    "old_value": "Test",
                    "new_value": "Test 2",
                },
                {
                    "property_name": "Status",
                    "old_value": "In progress",
                    "new_value": "Blocked",
                },
            ],
        )
    ],
}

"""
