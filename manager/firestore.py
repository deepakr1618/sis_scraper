import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
import base64
import time
import pyrebase

class Storage:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyAIob1OgzqrQ9v4-neTUtMLUOyyXX28jSk",
            "authDomain": "studentdetails-e2153.firebaseapp.com",
            "databaseURL": "https://studentdetails-e2153.firebaseio.com",
            "projectId": "studentdetails-e2153",
            "storageBucket": "studentdetails-e2153.appspot.com",
            "messagingSenderId": "125276779562",
            "appId": "1:125276779562:web:1bb5667d0979d9b71d7f53"
        };
        self.firebase = pyrebase.initialize_app(config)
        self.cred = credentials.Certificate('./manager/serviceAccount.json')
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def storeUsers(self , usn , dob , ph):
        phen = str(base64.b64encode(ph.encode()))[1:]
        doc_ref = self.db.collection(u'users').document(phen)
        doc_ref.set({
            u'usn': usn,
            u'dob': dob,
            u'phNo': ph
        })
    
    def storeAttendance(self, usn , dob, name , courses , attendance , pp , b64Img =""):
        self.usn = usn
        self.b64Img = b64Img
        doc_ref = self.db.collection(u'attendance').document(str(usn))
        doc_ref.set({
            u'usn': usn,
            u'dob': dob,
            u'lastScraped': time.time(),
            u'subjects' : courses,
            u'name': name,
            u'attendance' : attendance,
            u'proPic' : pp,
            u'imgSrc' : b64Img
        })
    def storeImage(self , imgPath):
        # client = self.db
        # bucket = client.bucket("users")
        # blob = bucket.blob(imgPath)
        # blob.upload_from_filename(imgPath)
        # return blob.public_url
        self.firebase.storage().child("images/"+self.usn+".png").put(imgPath)
        url = self.firebase.storage().child("images/"+self.usn+".png").get_url(None)
        return url
