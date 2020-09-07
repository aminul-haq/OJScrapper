from flask_pymongo import pymongo


class Database(object):
    URI = "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['fullstack']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update_one_set(collection, query, new_values):
        Database.DATABASE[collection].update_one_set(query, {"$set": new_values}, upsert=True)
