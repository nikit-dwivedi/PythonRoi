import datetime

from ..config.mongodb import db

partner_collection = db["partners"]
balance_collection = db["balances"]
transaction_collection = db["transactions"]

def DailyRoi():
    try:
        current_date = datetime.datetime.now() - datetime.timedelta(days=5)
        roi_partnership(current_date)
        return "roi updated"
    except Exception as e:
        print(e)
        return "something went wrong"

def roi_partnership(new_date):
    try:
        partnership_list = partner_collection.find({"createdAt": {"$lte": new_date}})
        for partnership in partnership_list:
            principle_amount = partnership["slabInfo"]["amount"]
            rate = partnership["slabInfo"]["interest"]
            time = 1
            SI = ((principle_amount * rate * time / 100) / 12) / 30
            print("_____________partner_________________")
            print(partnership)
            print(partnership["profit"]+SI)
            partner_collection.update_one({"_id": partnership["_id"]}, {"$set": {"profit": partnership["profit"] + SI}})
            custom_id = partnership["customId"]
            roi_balance(custom_id,SI)
            roi_transaction(custom_id,SI)
        return partnership_list
    except Exception as e:
        return "Error: " + str(e)

def roi_balance(custom_id,SI):
    try:
        balance_data = balance_collection.find_one({"customId": custom_id})
        print("_____________balance_________________")
        print(balance_data)
        print( balance_data["profit"]+SI)
        balance_collection.update_one({"_id": balance_data["_id"]}, {"$set": {"profit": balance_data["profit"] + SI}})
    except Exception as e:
        return "Error: " + str(e)

def roi_transaction(custom_id,SI):
    try:
        data = {
        "customId": custom_id,
        "type": "Credited",
        "amount": SI,
        "createdAt": datetime.datetime.utcnow(),
        "updatedAt": datetime.datetime.utcnow(),
        "__v":0
        }
        print("_____________transaction_________________")
        print(data)
        transaction_collection.insert_one(data)
    except Exception as e:
        return "Error: " + str(e)