from ..service.extended_style_service import ExtStyleService
from ..service.controlnet_service import ControlnetService
import gradio as gr


class ApplyUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)
        self.controlnet_service = ControlnetService(basedir)

    def apply_ext_style(self, style_name):
        style = self.ext_style_service.get_content(style_name)

        self.ext_style_service.apply_ext_style(style)

        controlnet = self.controlnet_service.get_content_by_extended_style_id(
            style['id'])

        return [
            style['prompt'],
            style['negative_prompt'],
            gr.Slider.update(
                value=int(style['width'])
            ),
            gr.Slider.update(
                value=int(style['height'])
            ),
            gr.Checkbox.update(
                value=True if controlnet is not None else False
            ),
            gr.Dropdown.update(
                value=controlnet['model'] if controlnet is not None else None
            ),
            gr.Image.update(
                value=controlnet['image'] if controlnet is not None else None
            ),
        ]
