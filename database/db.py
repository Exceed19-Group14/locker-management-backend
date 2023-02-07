from pymongo import MongoClient
import os
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URL)

try:
    conn = client.server_info()
    print('Connected to MongoDB')
except Exception:
    print('Unable to connect MongoDB')

db = client[MONGO_DB]
collection = db['lockers']
