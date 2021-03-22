import requests
import os 
from PIL import Image
import tempfile

def test_upload_picture_thumbnail_starting_size():
    image = Image.new('RGB', size=(128, 128))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post("http://localhost:5000/upload/",  files=files)
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"http://localhost:5000/uploadedfiles/{name}"
    expected_link_s = f"http://localhost:5000/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"http://localhost:5000/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m
    assert response.status_code == 200  
    os.remove(f'uploads/{name}')
    os.remove(f'uploads/s-thumbnail_{name}')
    os.remove(f'uploads/m-thumbnail_{name}')

def test_upload_picture_thumbnail_greater_size():
    image = Image.new('RGB', size=(129, 129))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post("http://localhost:5000/upload/",  files=files)
        # os.remove("uploads/test.png")
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"http://localhost:5000/uploadedfiles/{name}"
    expected_link_s = f"http://localhost:5000/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"http://localhost:5000/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m
    os.remove(f'uploads/{name}')
    os.remove(f'uploads/s-thumbnail_{name}')
    os.remove(f'uploads/m-thumbnail_{name}')

# Expect to provide thumbnails if any width/height are larger than 128
def test_upload_picture_thumbnail_width_smaller_height_larger_min():
    image = Image.new('RGB', size=(60, 129))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post("http://localhost:5000/upload/",  files=files)
        # os.remove("uploads/test.png")
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"http://localhost:5000/uploadedfiles/{name}"
    expected_link_s = f"http://localhost:5000/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"http://localhost:5000/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m
    os.remove(f'uploads/{name}')
    os.remove(f'uploads/s-thumbnail_{name}')
    os.remove(f'uploads/m-thumbnail_{name}')


