#here is where db stuff will go down to make things easy for us!
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

def get(db, col, q={}):
    return client[db][col].find_one(q)

def update(db, col, data, replace:bool=True):
    if replace:
        client[db][col].delete_many({})
        client[db][col].insert_one(data)
        return 
    client[db][col].insert_one(data)
    return

def list(db=None):
    if db is None:
        return client.list_database_names()
    return client[db].list_collection_names()