import modules.scripts as scripts
import gradio as gr
import os
import modules.shared as shared

from modules import images, script_callbacks, sd_models, sd_vae, prompt_parser, styles
from modules.processing import process_images, Processed
from modules.processing import Processed
from modules.shared import opts, cmd_opts, state
from modules.processing import StableDiffusionProcessing
from extensions.extended_styles.scripts.model.ext_styles import ExtStyles
from modules.ui import save_style_symbol, apply_style_symbol
from modules.ui_components import ToolButton


basedir = scripts.basedir()
ext_style_service = ExtStyles(basedir)


def gr_show(visible=True):
    return {"visible": visible, "__type__": "update"}


class ExtendedStyles(scripts.Script):
    dummy_component = None
    txt2img_width_component = None
    txt2img_height_component = None
    pos_prompt_component = None
    neg_prompt_component = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":  # postive prompt textbox
            self.pos_prompt_component = component
        if kwargs.get("elem_id") == "txt2img_neg_prompt":  # postive prompt textbox
            self.neg_prompt_component = component
        if kwargs.get("elem_id") == "txt2img_styles":  # postive prompt textbox
            pass
        if kwargs.get("elem_id") == "txt2img_width":
            self.txt2img_width_component = component
        if kwargs.get("elem_id") == "txt2img_height":
            self.txt2img_height_component = component

    # Extension title in menu UI

    def title(self):
        return "Extended Styles"

    # Decide to show menu in txt2img or img2img
    # - in "txt2img" -> is_img2img is `False`
    # - in "img2img" -> is_img2img is `True`
    #
    # below code always show extension menu
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        self.dummy_component = gr.Label(visible=False, value="sample")
        if self.pos_prompt_component is not None:
            self.ui_txt2img()

    # def add_extended_style(name: str, prompt: str, negative_prompt: str):
    #     if name is None:
    #         return [gr_show() for x in range(4)]

    #     style = styles.PromptStyle(name, prompt, negative_prompt)
    #     shared.prompt_styles.styles[style.name] = style
    #     # Save all loaded prompt styles: this allows us to update the storage format in the future more easily, because we
    #     # reserialize all styles every time we save them
    #     shared.prompt_styles.save_styles(shared.styles_filename)

    #     return [gr.Dropdown.update(visible=True, choices=list(shared.prompt_styles.styles)) for _ in range(2)]

    def apply_ext_style(self, index):
        style = ext_style_service.get_content(index)
        # shared.opts.data['sd_model_checkpoint'] = '2.5D_orangechillmix_v70Fixed.safetensors [5447484f4c]'
        # shared.opts.data['sd_vae'] = 'vae-ft-mse-840000-ema-pruned.safetensors'

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

        return [
            style['prompt'],
            style['negative_prompt'],
            gr.Slider.update(
                value=style['width']
            ),
            gr.Slider.update(
                value=style['height']
            )]

    # cf. https://discuss.huggingface.co/t/how-to-update-the-gr-dropdown-block-in-gradio-blocks/19231
    def filter_ext_style(self):
        styles = ext_style_service.get_contents()
        filtered_styles = [style for style in styles if (
            style['sd_model_checkpoint'] == shared.opts.data['sd_model_checkpoint']) and (style['sd_vae'] == shared.opts.data['sd_vae'])]
        # dropdown.choices = filtered_choices
        filtered_choices = ext_style_service.get_choices(filtered_styles)
        return gr.Dropdown.update(
            choices=filtered_choices,
            value=filtered_choices[0],
        )

    def filter_ext_style_clear(self):
        choices = ext_style_service.get_choices()
        return gr.Dropdown.update(
            choices=choices,
            value=choices[0],
        )

    def ui_txt2img(self):

        # script_callbacks.on_after_component(self.after_component)

        with gr.Accordion('Extended Styles', open=True):
            with gr.Row():
                choices = ext_style_service.get_choices()
                ext_style_dropdown = gr.Dropdown(
                    choices=choices,
                    type='index',
                    value=choices[0],
                    label="select extended style"
                )
                applay_button = ToolButton(
                    value=apply_style_symbol,
                    elem_id="extended_style_apply",
                )
                applay_button.click(
                    fn=self.apply_ext_style,
                    inputs=ext_style_dropdown,
                    outputs=[self.pos_prompt_component,
                             self.neg_prompt_component,
                             self.txt2img_width_component,
                             self.txt2img_height_component
                             ]
                )

            with gr.Row():
                filter_button = gr.Button(
                    value='current model filter'
                )
                filter_button.click(
                    fn=self.filter_ext_style,
                    inputs=[],
                    outputs=ext_style_dropdown
                    # inputs=[ext_style_dropdown, shared.opts.data['sd_model_checkpoint'],
                    #         shared.opts.data['sd_vae']],
                    # outputs=ext_style_dropdown
                )
                filter_clear_button = gr.Button(
                    value='filter_clear'
                )
                filter_clear_button.click(
                    fn=self.filter_ext_style_clear,
                    inputs=[],
                    outputs=ext_style_dropdown
                )

            with gr.Accordion('Save', open=False):
                with gr.Row():
                    def add_extended_style(name: str):
                        log(name)

                        style = {
                            'name': name,
                            'sd_model_checkpoint': shared.opts.data['sd_model_checkpoint'],
                            'sd_vae': shared.opts.data['sd_vae'],
                            'prompt': self.pos_prompt_component.value,
                            'negative_prompt': self.neg_prompt_component.value,
                            'width': self.txt2img_width_component.value,
                            'height': self.txt2img_height_component.value
                        }
                        ext_style_service.save(style)
                        choices = ext_style_service.get_choices()
                        return gr.Dropdown.update(
                            choices=choices,
                            value=choices[-1])

                    save_style_button = ToolButton(
                        value=save_style_symbol,
                        elem_id="extended_style_create",
                    )
                    save_style_button.click(
                        fn=add_extended_style,
                        _js="ask_for_extended_style_name",
                        # Have to pass empty dummy component here, because the JavaScript and Python function have to accept
                        # the same number of parameters, but we only know the style-name after the JavaScript prompt
                        inputs=[self.dummy_component],
                        outputs=ext_style_dropdown,
                    )


def log(text: str):
    print(f"[Externded Styles] {text}")
