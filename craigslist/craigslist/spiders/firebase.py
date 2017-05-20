#firebase integration
import pyrebase

#Firebase config
config = {
        "apiKey": "AIzaSyDQo_48l06qVMGbOIsGzftxKznq85x2IBE",
        "authDomain": "spiderbike-36fa3.firebaseapp.com",
        "databaseURL": "https://spiderbike-36fa3.firebaseio.com",
        "storageBucket": "projectId.appspot.com",
        "serviceAccount":"/Users/vyas45/Desktop/Code/Projects/motorCraig/spiderBike/craigsBike-7773be87a457.json"
        }

def db_init():
    firebase  = pyrebase.initialize_app(config)
    auth = firebase.auth()
    email = 'vyas45@gmail.com'
    password = 'firebase'
    user = auth.sign_in_with_email_and_password(email, password)
    db = firebase.database()
    return db, user


