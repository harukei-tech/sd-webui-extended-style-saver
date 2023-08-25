from ..service.extended_style_service import ExtStyleService
import gradio as gr
import modules.shared as shared
from modules import sd_models, sd_vae


class ApplyUsecase():
    def __init__(self, basedir) -> None:
        self.ext_style_service = ExtStyleService(basedir)

    def apply_ext_style(self, style_name):
        style = self.ext_style_service.get_content(style_name)

        if (shared.opts.data['sd_model_checkpoint'] != style['sd_model_checkpoint']):
            if style['sd_model_checkpoint'] is not None and style['sd_model_checkpoint'] not in sd_models.checkpoints_list:
                raise RuntimeError(
                    f"model {style['sd_model_checkpoint']!r} not found")
            shared.opts.data['sd_model_checkpoint'] = style['sd_model_checkpoint']
            shared.opts.set("sd_model_checkpoint",
                            style['sd_model_checkpoint'])
            sd_models.reload_model_weights()

        if (shared.opts.data['sd_vae'] != style['sd_vae']):
            pass
            shared.opts.data['sd_vae'] = style['sd_vae']
            shared.opts.set("sd_vae", style['sd_vae'])
            sd_vae.reload_vae_weights()


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
        ]
