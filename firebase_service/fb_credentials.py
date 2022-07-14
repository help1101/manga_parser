import firebase_admin
from firebase_admin import credentials


class Credentials:
    cred = credentials.Certificate('accountKey.json')
    config = {
        "apiKey": "AIzaSyBRb7GbYTNLZ24VzjFuAJX_5EysSWPjMo0",
        "authDomain": "manga-app-222cd.firebaseapp.com",
        "databaseURL": "https://manga-app-222cd-default-rtdb.europe-west1.firebasedatabase.app",
        "projectId": "manga-app-222cd",
        "storageBucket": "manga-app-222cd.appspot.com",
        "messagingSenderId": "901546834306",
        "appId": "1:901546834306:web:4f2129fecf2b58e859779b",
        "measurementId": "G-F66D98EEVZ"
    }
    app = firebase_admin.initialize_app(cred, config)




