import requests
import os 
from PIL import Image
import tempfile
from flask import current_app as app

def test_upload_picture_small_no_thumbnail():
    image = Image.new('RGB', size=(127, 127))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"http://{localhost:5000}/upload/",  files=files)
    name = file.name.rsplit("/", 1)[1]
    expected_link= f"http://localhost:5000/uploadedfiles/{name}"
    json_body = response.json()

    has_small_thumbnail = True 
    has_med_thumbnail = True 

    if 'small_thumbnail' in json_body:
        has_small_thumbnail  = False
    if 'med_thumbnail' in json_body:
        has_med_thumbnail  = False
    

    assert response.json()["original"] == expected_link
    assert has_small_thumbnail
    assert has_med_thumbnail
    assert response.status_code == 200  
    os.remove(f'uploads/{name}')


def test_uploadedfiles_link():
    files = {'file': ('test.png', 'testFile')}
    requests.post("http://localhost:5000/upload/", files=files)
    response = requests.get("http://localhost:5000/uploadedfiles/test.png")
    assert response .status_code == 200  
    os.remove("uploads/test.png")

def test_upload_picture_no_file():
    files = {'file': ('', '')}
    response = requests.post("http://localhost:5000/upload/", files=files)
    assert response.status_code == 400  

def test_upload_picture_not_accepted_extension_1():
    files = {'file': ('test.pdf', 'test')}
    response = requests.post("http://localhost:5000/upload/", files=files)
    assert response.status_code == 400  

def test_upload_picture_not_accepted_extension_not_uploaded():
    response = requests.get("http://localhost:5000/uploadfiles/test.pdf")
    assert response.status_code == 404  

def test_upload_picture_not_accepted_extension_2():
    files = {'file': ('file', 'test')}
    response = requests.post("http://localhost:5000/upload/", files=files)
    assert response.status_code == 400  

def test_upload_picture_not_accepted_extension_3():
    files = {'file': ('.png_file', 'test')}
    response = requests.post("http://localhost:5000/upload/", files=files)
    print(response)
    assert response.status_code == 400  