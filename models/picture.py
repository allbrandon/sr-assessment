from mongoengine import Document, StringField, FileField


class Picture(Document):
    picture = FileField()
    image_url = StringField()