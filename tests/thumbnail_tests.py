import requests
import os 
from PIL import Image
import tempfile
url = "https://pure-hamlet-32179.herokuapp.com"

def test_upload_picture_thumbnail_starting_size():
    image = Image.new('RGB', size=(128, 128))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{url}/upload/",  files=files)
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"{url}/uploadedfiles/{name}"
    expected_link_s = f"{url}/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"{url}/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m
    assert response.status_code == 200  

def test_upload_picture_thumbnail_greater_size():
    image = Image.new('RGB', size=(129, 129))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{url}/upload/",  files=files)
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"{url}/uploadedfiles/{name}"
    expected_link_s = f"{url}/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"{url}/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m

# Expect to provide thumbnails if any width/height are larger than 128
def test_upload_picture_thumbnail_width_smaller_height_larger_min():
    image = Image.new('RGB', size=(60, 129))
    file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(file)
    with open(file.name, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{url}/upload/",  files=files)
        # os.remove("uploads/test.png")
    name = file.name.rsplit("/", 1)[1]
    expected_link_original = f"{url}/uploadedfiles/{name}"
    expected_link_s = f"{url}/uploadedfiles/s-thumbnail_{name}"
    expected_link_m = f"{url}/uploadedfiles/m-thumbnail_{name}"

    json_body = response.json()

    assert json_body["original"] == expected_link_original 
    assert json_body["small_thumbnail"] == expected_link_s
    assert json_body["med_thumbnail"] == expected_link_m



