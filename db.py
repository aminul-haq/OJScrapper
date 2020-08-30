from flask_pymongo import pymongo


# CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority"
# client = pymongo.MongoClient(CONNECTION_STRING)
# db = client.get_database('test')
# user_collection = pymongo.collection.Collection(db, 'test')

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority")
db = client.get_database("test")

print(db.list_collection_names())

# #doc = db.test.insert({'abcd': 'abcd'})
# cars = [{'name': 'Audi', 'price': 52642},
#             {'name': 'MercedesX', 'price': 57127},
#             {'name': 'SkodaX', 'price': 9000},
#             {'name': 'VolvoX', 'price': 29000},
#             {'name': 'BentleyX', 'price': 350000},
#             {'name': 'CitroenX', 'price': 21000},
#             {'name': 'HummerX', 'price': 41400},
#             {'name': 'VolkswagenX', 'price': 21600}]
# x = db.test.insert_many(cars)
# print(x)

