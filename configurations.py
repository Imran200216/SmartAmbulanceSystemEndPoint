import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()