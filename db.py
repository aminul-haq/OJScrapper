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

'''
@app.route("/dbtest")
def test():
    # client = pymongo.MongoClient(
    #     "mongodb+srv://admin:admin@cluster0.s022h.mongodb.net/test?retryWrites=true&w=majority")
    # db = client.get_database("test")

    print(database.db.list_collection_names())

    return "Connected to the data base!"


@app.route("/dbinsert/<string:car_price>", methods=["GET"])
def insert(car_price):
    splitted = car_price.split("_")
    model = splitted[0]
    price = int(splitted[1])
    database.db.test.insert_one({"name": model, "price": price})
    return "inserted"


@app.route("/dbquery/price/<string:model>", methods=["GET"])
def get_price(model):
    res = database.db.test.find({"name": model})
    res_list = [x for x in res]
    return Response(json.dumps(res_list,default=str),mimetype="application/json")

'''