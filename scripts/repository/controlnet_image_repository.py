from ..lib.image_accesser import ImageAccesser
import uuid


class ControlnetImageRepository():
    ImageAccesser: ImageAccesser

    def __init__(self, basedir) -> None:
        self.accesser = ImageAccesser(basedir)

    def save(self, image):
        new_file_name = uuid.uuid4().hex + '.jpg'
        self.accesser.save(image=image, fileName=new_file_name)
        return new_file_name

    def get_content(self, file_name):
        return self.accesser.encodeToNumpy(file_name)
