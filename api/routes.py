from api.upload import UploadApi
from api.uploadedfiles import UploadedFilesApi



def create_routes(api):
    api.add_resource(UploadApi, '/upload/')
    api.add_resource(UploadedFilesApi, '/uploadedfiles/<filename>')


