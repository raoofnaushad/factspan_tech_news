from datetime import date, datetime
from pymongo import MongoClient

from libs.config import *

today = str(date.today())

try:
    conn = MongoClient()
    print("Connected successfully to MongoDB")
except:  
    print("Could not connect to MongoDB")

# database
db = conn.social_media_automation

def get_data_from_mongo(date):
    # collection = db.news
    collection = db.newsgpt
    data = collection.find({"date" : date}) #initially it was today
    data = [d for d in data]
    print(f"Data found from mongo for the date: {today}")
    return data

def get_full_from_mongo(article):
    collection = db.newsgpt
    data = collection.find({"article" : article}) #initially it was today
    try:
        data = [d for d in data][0]
        data["texts"] = data["text"].split('\n')
        print(f"Data found from mongo for the article: {article}")
        return data
    except Exception as e:
        print(f"Error: {e}")
        return {}


def add_subscribers(name, email):
    try:
        subscriber = {
            "name" : name,
            "email" : email
            }
        collection = db.subscribers
        rec_id1 = collection.insert_one(subscriber)
        print(f"Inserted a new subscriber <> name: {name}, email: {email}")
    except Exception as ex:
        print(f"Error in adding the subscriber: {ex}")

def remove_subscribers(email):
    try:
        subscriber = {
            "email" : email
            }
        collection = db.subscribers
        rec_id1 = collection.delete_one(subscriber)
        print(f"Deleted subscriber <> email: {email}")
    except Exception as ex:
        print(f"Error in adding the subscriber: {ex}")