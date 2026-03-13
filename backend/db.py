from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["cyber_safety_db"]

moderation_logs = db["moderation_logs"]