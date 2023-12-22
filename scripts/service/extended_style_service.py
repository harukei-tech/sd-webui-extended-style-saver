from ..repository.ext_style_repository import ExtStyleRepository
import gradio as gr
import modules.shared as shared
from modules import sd_models, sd_vae
import uuid


class ExtStyleService():
    ext_style_repository = None

    def __init__(self, basedir) -> None:
        self.ext_style_repository = ExtStyleRepository(basedir)

    # cf. https://discuss.huggingface.co/t/how-to-update-the-gr-dropdown-block-in-gradio-blocks/19231
    def filter_ext_style(self):
        styles = self.ext_style_repository.get_contents()
        filtered_styles = [style for style in styles if (
            style['sd_model_checkpoint'] == shared.opts.data['sd_model_checkpoint']) and (style['sd_vae'] == shared.opts.data['sd_vae'])]
        filtered_choices = self.get_choices(
            filtered_styles)
        return gr.Dropdown.update(
            choices=filtered_choices,
        )

    def refresh(self):
        choices = self.get_choices()

        return gr.Dropdown.update(
            choices=choices,
        )

    def save(self, name: str, pos_prompt_component, neg_prompt_component, txt2img_width_component, txt2img_height_component):
        style = {
            'id': uuid.uuid4().hex,
            'name': name,
            'sd_model_checkpoint': shared.opts.data['sd_model_checkpoint'],
            'sd_vae': shared.opts.data['sd_vae'],
            'prompt': pos_prompt_component,
            'negative_prompt': neg_prompt_component,
            'width': txt2img_width_component,
            'height': txt2img_height_component,
        }
        self.ext_style_repository.save(style)
        choices = self.get_choices()
        return (gr.update(
            choices=choices,
            value=choices[-1]), style.get('id'))

    def delete(self, id):
        self.ext_style_repository.delete(id)
        choices = self.get_choices()
        return gr.update(
            choices=choices,
            value=''
        )

    def apply_ext_style(self, style):

        if (shared.opts.data['sd_model_checkpoint'] != style['sd_model_checkpoint']):
            if style['sd_model_checkpoint'] is not None and style['sd_model_checkpoint'] not in sd_models.checkpoints_list:
                raise RuntimeError(
                    f"model {style['sd_model_checkpoint']!r} not found")
            shared.opts.data['sd_model_checkpoint'] = style['sd_model_checkpoint']
            shared.opts.set("sd_model_checkpoint",
                            style['sd_model_checkpoint'])
            sd_models.reload_model_weights()

        if (shared.opts.data['sd_vae'] != style['sd_vae']):
            shared.opts.data['sd_vae'] = style['sd_vae']
            shared.opts.set("sd_vae", style['sd_vae'])
            sd_vae.reload_vae_weights()

    def get_choices(self, styles=None):
        return self.ext_style_repository.get_choices(styles)

    def get_content(self, style_name):
        return self.ext_style_repository.get_content(style_name)
