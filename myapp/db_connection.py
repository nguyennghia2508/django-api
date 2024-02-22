from dotenv import load_dotenv
import pymongo
import os
load_dotenv()

if os.getenv("MONGODB_URI"):
    url = os.getenv('MONGODB_URI')
    print("Connect db success to production")
else:
    url = 'mongodb://localhost:27017'
    print("Connect db success to development")

client = pymongo.MongoClient(url)

db = client['ShopCart']

