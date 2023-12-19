

from pymongo.mongo_client import MongoClient
import datetime
post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.now(tz=datetime.timezone.utc),
}

uri = "mongodb+srv://sahil:gZrTSwnfaex5I2IE@hackton.u1vq7f7.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["sih"]
collection = db["driver_data"]

post_id = collection.insert_one(post)
print(post_id)