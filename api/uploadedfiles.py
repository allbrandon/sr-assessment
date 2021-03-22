from flask import send_from_directory
from flask import current_app as app
from flask_restx import Resource


class UploadedFilesApi(Resource):
    def get(self, filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)