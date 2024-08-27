import os
from dotenv import load_dotenv
from databases import Database

load_dotenv()

db_connection = Database(os.environ['PG_URL'])
