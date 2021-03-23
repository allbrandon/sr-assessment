# flask packages
import os
from flask import jsonify, render_template, request, make_response, redirect, url_for 
from flask_restx import Resource
from werkzeug.utils import secure_filename
from flask import current_app as app
import zipfile
from io import BytesIO
from werkzeug.datastructures import FileStorage
from PIL import Image


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'zip'}
# check if the extension is part of the accepted set/has an extension
def accepted_file(filename): 
    if '.' in filename and '/' not in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True 
    return False

# Make a thumbnail given the desired width, will keep aspect ratio and return the new filename
def generateThumbnail(image, new_width, original_filename, prefix):
    
    width, height = image.size
    new_height = new_width * height / width
    thumbnail = image.resize((new_width, int(round(new_height))))
    filename = prefix + original_filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    thumbnail.save(path)

    return filename
# For uploading one image
def uploadSingle(f, filename):
    images = {}
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(path)

    with Image.open(path) as img:
        width, height = img.size

        if width >= 128 or height >= 128:
            small_thumbnail_name = generateThumbnail(img, 32, filename, 's-thumbnail_')
            images["small_thumbnail"] = url_for('uploaded_files_api', filename=small_thumbnail_name, _external=True)

            med_thumbnail_name = generateThumbnail(img, 64, filename, 'm-thumbnail_')
            images["med_thumbnail"] = url_for('uploaded_files_api', filename=med_thumbnail_name, _external=True)

    images["original"] = url_for('uploaded_files_api', filename=filename, _external=True)
    return images

# For uploading multiple images in a zip, ignores non image files
def uploadZip(zip):
    urls = []
    filebytes = BytesIO(zip.read())
    myzipfile = zipfile.ZipFile(filebytes)
    for filename in myzipfile.namelist():
        if accepted_file(filename):
            filename = secure_filename(filename)
            file = FileStorage(BytesIO(myzipfile.read(filename)))
            urls.append(uploadSingle(file, filename))
    return urls

class UploadApi(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('upload.html'),200,headers)

    def post(self):
        f = request.files['file']
        # No file 
        if f.filename == "": 
            return 'Error: No file uploaded', 400
        # File is as expected 
        elif accepted_file(f.filename):
            fileExt = f.filename.rsplit('.', 1)[1].lower()
            # check as user filenames cannot be trusted
            filename = secure_filename(f.filename)

            if fileExt == "zip": 
                return uploadZip(f), 200
            else:
                return uploadSingle(f, filename), 200
        else: 
            return 'Error: File is not a picture or zip file', 400

            
