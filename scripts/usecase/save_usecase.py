from ..service.extended_style_service import ExtStyleService
from ..service.controlnet_service import ControlnetService


class SaveUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)
        self.controlnet_service = ControlnetService(basedir)

    def save(self, name: str, pos_prompt_component, neg_prompt_component, txt2img_width_component, txt2img_height_component, controlnet_enabled, controlnet_model, controlnet_input_image_components, controlnet_generated_image_components):
        gr, extended_style_id = self.ext_style_service.save(
            name=name,
            pos_prompt_component=pos_prompt_component,
            neg_prompt_component=neg_prompt_component,
            txt2img_width_component=txt2img_width_component,
            txt2img_height_component=txt2img_height_component,
        )

        if controlnet_enabled:
            controlnet_id = self.controlnet_service.save(
                extended_style_id=extended_style_id,
                model=controlnet_model,
                input_image=controlnet_input_image_components,
                generated_image=controlnet_generated_image_components,
            )

        return gr
