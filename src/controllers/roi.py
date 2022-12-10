from firebase_admin import firestore
from flask import request
from ..config.fb import initDb


authString = '11aab4ed5a28f5c6c4f44af7d1249b686737f16bae499f351162ffedb7e2d093'


def welcome():
    data = request.json
    if data["auth"] == authString:
        portfolioRef = initDb.collection("PORTFOLIO")
        print("_______________")
        portfolioList = portfolioRef.get()
        for portfolio in portfolioList:
            print("uid", portfolio.to_dict()["uid"])
            getAndUpdatePortfolioProfit(portfolio.to_dict()["uid"], portfolio.id)
    return "done"


def getAndUpdatePortfolioProfit(user_id, port_id):
    portRef = initDb.collection('PORTFOLIO').document(port_id)

    try:

        portDoc = portRef.get()
        amount = portDoc.to_dict()["amount"]
        rate = portDoc.to_dict()["rate"]

        interestMonthly = (amount * rate) / 100
        interestDaily = interestMonthly / 30
        newProfit = portDoc.to_dict()["profit"] + interestDaily
        print("---------------------------------------portfolio------------------------------------------")
        print("old profit======>", portDoc.to_dict()[
              "profit"], "new profit======>", newProfit)
        portRef.update({"profit": newProfit})
        createTransaction(user_id, interestDaily)

    except Exception as error:

        print(error)


def createTransaction(user_id, amount):
    transactionID = initDb.collection('PORTFOLIO').document().id
    initDb.collection('TRANSACTION').document(transactionID).set({
        "id": transactionID,
        "amount": amount,
        "reason": "Daily interest",
        "status": 2,
        "type": 2,
        "uid": user_id,
        "timestamp": firestore.SERVER_TIMESTAMP
    })
    getAndUpdateWalletBalance(user_id, amount)


def getAndUpdateWalletBalance(user_id, interestDaily):
    balRef = initDb.collection('BALANCE').document(user_id)
    try:
        balDoc = balRef.get()
        newProfit = balDoc.to_dict()["profit"] + interestDaily
        balRef.update({"profit": newProfit})
        print("---------------------------------------balance------------------------------------------")
        print("old profit======>", balDoc.to_dict()[
              "profit"], "new profit======>", newProfit)
        print("Success! for UID==>", user_id)
        print("_____________________________________________________________done_____________________________________________________________")

    except Exception as e:
        print(e)


# def getAndUpdateWalletBalance(user_id, interestDaily):
#     balRef = initDb.collection('BALANCE').document(user_id)
#     try:
#         balDoc = balRef.get()
#         print("balDoc",balDoc)
#         print("data",balDoc.to_dict())
#         print("_____________________________________________________________done_____________________________________________________________")

#     except Exception as e:
#         print(e)
