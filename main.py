from dotenv import load_dotenv
from notion_client import Client
from typing import Dict
from classes import ChangeSet, Page
from webhook import generate_message, send_message
from display import changeset_timeout 
import os
from utils import parse_db_query_response, identify_changes
from time import sleep
from datetime import timedelta
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

"""
We identify the new changes in every polling interval.
If there are new changes, we apply to the changeset.
Then, if the changeset is non-empty, we try to generate a message:
    Specifically, the message is only non-empty if there is any expired fields
    Then send message if message is non-empty
Set new state and poll again.
"""

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    logger = logging.getLogger()
    polling_interval = int(os.environ.get("NOTION_POLLING_INTERVAL_SECONDS", 60))
    timeout = timedelta(minutes=2)
    prev_state = []
    prev_state = get_state()
    changeset = ChangeSet([], [], {})

    while True:
        new_state = get_state()
        new_changeset = identify_changes(prev_state, new_state)

        if new_changeset.is_empty():
            logger.info("No changes detected")
            
        else:
            changeset.merge_set(new_changeset)
            logger.info("Changes detected.")
        
        if not(changeset.is_empty()):
            messages = changeset_timeout(changeset, timeout, new_state)
            message = generate_message(messages)

            # Expect message == "" if there is nothing returned from generate_message
            if message != "":
                logger.info("Message sent.")
                send_message(message)

        prev_state = new_state
        sleep(polling_interval)


if __name__ == "__main__":
    main()
