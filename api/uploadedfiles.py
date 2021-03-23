from flask import send_from_directory
from flask import current_app as app
from flask_restx import Resource
import os 

MYDIR = os.path.dirname(__file__)

class UploadedFilesApi(Resource):
    def get(self, filename):
        return send_from_directory(MYDIR + "/" + app.config['UPLOAD_FOLDER'],
                               filename)