
import os
from PIL import Image
import numpy as np


class ImageAccesser():
    base_dir = ''
    image_dir = '/scripts/image/openpose'

    def __init__(self, base_dir) -> None:
        self.base_dir = base_dir.replace(
            os.path.sep, '/') + '/' + self.image_dir

    def save(self, image, fileName):
        path = self.base_dir + '/' + fileName
        pil_img = self.decodeFromNumpy(image)
        pil_img.save(path)

    def decodeFromNumpy(self, image):
        return Image.fromarray(image)

    def encodeToNumpy(self, imageFile):
        path = self.base_dir + '/' + imageFile
        return np.array(Image.open(path))
