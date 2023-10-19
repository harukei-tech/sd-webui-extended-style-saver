from ..repository.controlnet_repository import ControlnetRepository
from ..repository.controlnet_image_repository import ControlnetImageRepository
import uuid


class ControlnetService():
    csvRepository = None
    imageRepository = None

    def __init__(self, basedir) -> None:
        self.csvRepository = ControlnetRepository(basedir)
        self.imageRepository = ControlnetImageRepository(basedir)

    # Multiple Controlnet units are not supported.
    # gradio interface's inputs key does not support varargs
    def save(self, extended_style_id, model, input_image, generated_image):
        if (input_image is None and generated_image is None):
            return None

        generated_file_name = (self.imageRepository.save(generated_image)
                               if generated_image is not None
                               else None)
        if generated_file_name is None:
            input_file_name = (self.imageRepository.save(input_image['image'])
                               if input_image is not None
                               else None)

        image = generated_file_name if generated_file_name is not None else input_file_name

        row = {
            'id': uuid.uuid4().hex,
            'extended_style_id': extended_style_id,
            'model': model,
            'image': image,
        }
        self.csvRepository.save(row)
        return row['id']

    def get_content_by_extended_style_id(self, extended_style_id):
        rows = self.csvRepository.get_contents(extended_style_id)
        if len(rows) == 0:
            return None

        row = rows[0]
        image = self.imageRepository.get_content(
            self.csvRepository.get_image_name(row))

        return {
            'id': row['id'],
            'model': row['model'],
            'image': image,
        }
