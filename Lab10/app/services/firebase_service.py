import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("firebase.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': '<identifier>.firebasestorage.app'
})
bucket = storage.bucket()