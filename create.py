import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc = {
  "name": "黃玟瑄",
  "mail": "s1114670@pu.edu.tw",
  "lab": 402
}

#doc_ref = db.collection("靜宜資管").document("xuan")
#doc_ref.set(doc)
collection_ref = db.collection("靜宜資管")
collection_ref.add(doc)