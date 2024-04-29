from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "<DATABASE_URI>"
client = MongoClient(uri, server_api=ServerApi('1'))

mongoDatabase = client["<DATABASE_NAME>"]
mongoCollection = mongoDatabase["<COLLECTION_NAME>"]

