from dotenv import load_dotenv
from notion_client import Client
from typing import Dict
import os
from utils import parse_db_query_response, identify_changes

load_dotenv()

notion = Client(auth=os.environ["NOTION_TOKEN"])


def get_database_data() -> Dict:
    db = notion.databases.query(database_id=os.environ["NOTION_DATABASE_ID"])
    return db # type: ignore

def main():

    data =  get_database_data()

    old_data = parse_db_query_response(data)
    input("Make changes to the db then press enter to continue")
    
    data =  get_database_data()

    new_data = parse_db_query_response(data)

    changes = identify_changes(old_data, new_data)

    print(changes)


if __name__ == "__main__":
    main()
