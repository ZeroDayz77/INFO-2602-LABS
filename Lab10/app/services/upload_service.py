import os, string, random
from .firebase_service import bucket


class UploadService:
    def random_string():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    async def store_file(self, file):
        extension = os.path.splitext(file.filename)[1]
        newname = self.random_string() + extension
        blob = bucket.blob(newname)
        blob.upload_from_file(file.file)
        return newname
    
    def list_files():
        return os.listdir('uploads')
    
    def views_file(filename):
        return os.path.join('uploads', filename)


    def remove_file(self, filename):
        try:
            blob = bucket.blob(filename)
            blob.delete()
        except Exception:
            print('file already Deleted from Firebase')