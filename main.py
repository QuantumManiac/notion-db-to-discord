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

        sleep(int(os.environ["NOTION_POLLING_INTERVAL_SECONDS"]))

if __name__ == "__main__":
    main()
