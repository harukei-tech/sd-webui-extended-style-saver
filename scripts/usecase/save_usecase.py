from ..service.extended_style_service import ExtStyleService


class SaveUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)

    def save(self, name: str, pos_prompt_component, neg_prompt_component, txt2img_width_component, txt2img_height_component):
        gr, extended_style_id = self.ext_style_service.save(
            name=name,
            pos_prompt_component=pos_prompt_component,
            neg_prompt_component=neg_prompt_component,
            txt2img_width_component=txt2img_width_component,
            txt2img_height_component=txt2img_height_component,
        )

        return gr
