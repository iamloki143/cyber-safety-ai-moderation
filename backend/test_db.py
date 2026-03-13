from pymongo import MongoClient
import ssl

MONGO_URL = "mongodb+srv://lokeshs14032005_db_user:jaisurya29lokesh48@cluster0.klmmp6k.mongodb.net/?appName=Cluster0"

client = MongoClient(
    MONGO_URL,
    tls=True,
    tlsAllowInvalidCertificates=True
)

db = client["cyber_safety"]

print("Databases:", client.list_database_names())

collection = db["messages"]

sample = {"user": "lokesh", "text": "DB test successful"}
collection.insert_one(sample)

print("Inserted successfully")
