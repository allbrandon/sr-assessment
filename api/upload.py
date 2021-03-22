# flask packages
import os
from flask import jsonify, render_template, request, make_response, redirect, url_for 
from flask_restx import Resource
from werkzeug.utils import secure_filename
from flask import current_app as app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# mongo-engine models
from models.picture import Picture

def accepted_file(filename): 
    if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True 
    return False

class UploadApi(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        
        return make_response(render_template('upload.html'),200,headers)
    def post(self):
        f = request.files['file']

        if f.filename == "": 
            return 'Error: No file uploaded' 
        elif accepted_file(f.filename):
            picture = Picture(image_url=f.filename) 
            fileExt = f.filename.rsplit('.', 1)[1].lower()

            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return url_for('uploaded_files_api',
                                    filename=filename, _external=True)
            # with open(f.filename, 'rb') as image_file:
                
            #     picture.put(image_file,content_type='image/{fileExt}')
            # picture.save()
            # return 'fiel uploaded sucesfullay'
        else: 
            return 'Error: file is not a picture'

            
