from flask_pymongo import pymongo
import json


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
    def remove(collection, query):
        return Database.DATABASE[collection].remove(query)

    @staticmethod
    def remove_one(collection, query):
        return Database.DATABASE[collection].remove_one(query)

    @staticmethod
    def get_all_records(collection):
        return list(Database.DATABASE[collection].find())

    @staticmethod
    def get_all_records(collection, query):
        return list(Database.DATABASE[collection].find(query))

    @staticmethod
    def update_one_set(collection, query, new_values):
        Database.DATABASE[collection].update_one(query, {"$set": new_values}, upsert=True)

# if __name__ == '__main__':
#     Database.initialize()
#     data = Database.get_all_records("users")
#     print(data)
#     print()
