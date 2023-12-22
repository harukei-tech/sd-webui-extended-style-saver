from ..service.extended_style_service import ExtStyleService


class DeleteUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)

    def delete(self, id):
        gr = self.ext_style_service.delete(id)
        return gr
