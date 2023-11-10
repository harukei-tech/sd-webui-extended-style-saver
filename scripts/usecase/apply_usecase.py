from ..service.extended_style_service import ExtStyleService
import gradio as gr


class ApplyUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)

    def apply_ext_style(self, style_name):
        style = self.ext_style_service.get_content(style_name)

        self.ext_style_service.apply_ext_style(style)

        return [
            style['prompt'],
            style['negative_prompt'],
            gr.Slider.update(
                value=int(style['width'])
            ),
            gr.Slider.update(
                value=int(style['height'])
            ),
        ]
