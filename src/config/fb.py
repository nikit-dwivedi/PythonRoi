# import firebase_admin
# from firebase_admin import credentials



import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('src/config/firebaseConfig.json')
# Use the application default credentials.

firebase_admin.initialize_app(cred)
initDb = firestore.client()