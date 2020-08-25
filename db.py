from flask import Flask
from flask_pymongo import pymongo
from app import app

# CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('test')
# user_collection = pymongo.collection.Collection(db, 'test')

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("test")
db.co

print(db.list_collection_names())
