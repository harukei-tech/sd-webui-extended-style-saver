import gradio as gr

import modules.scripts as scripts
from scripts.service.extended_style_service import \
    ExtStyleService
from scripts.usecase.save_usecase import SaveUsecase
from scripts.usecase.apply_usecase import ApplyUsecase
from modules.ui import refresh_symbol, apply_style_symbol, save_style_symbol
from modules.ui_components import ToolButton

basedir = scripts.basedir()
save_usecase = SaveUsecase(basedir)
apply_usecase = ApplyUsecase(basedir)
ext_style_service = ExtStyleService(basedir)

filter_symbol = '\U0001f3af'  # dart


class ExtendedStyles(scripts.Script):
    dummy_component = None
    txt2img_width_component = None
    txt2img_height_component = None
    pos_prompt_component = None
    neg_prompt_component = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    # this function will be called automaticaly
    def after_component(self, component, **kwargs):
        if kwargs.get("elem_id") == "txt2img_prompt":  # postive prompt textbox
            self.pos_prompt_component = component
        elif kwargs.get("elem_id") == "txt2img_neg_prompt":  # negative prompt textbox
            self.neg_prompt_component = component
        elif kwargs.get("elem_id") == "txt2img_styles":  # style prompt textbox
            pass
        elif kwargs.get("elem_id") == "txt2img_width":
            self.txt2img_width_component = component
        elif kwargs.get("elem_id") == "txt2img_height":
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

    def ui_txt2img(self):
        with gr.Accordion('Extended Styles', open=True):
            # extended_style selection
            with gr.Row():
                choices = ext_style_service.get_choices()

                filter_button = ToolButton(
                    value=filter_symbol,
                    elem_id="extended_style_filter",
                )

                ext_style_dropdown = gr.Dropdown(
                    choices=choices,
                    # type="index", #gradio3 has bug
                    label="select extended style",
                    elem_id="extended_style_styles",
                )

                filter_button.click(
                    fn=ext_style_service.filter_ext_style,
                    inputs=[],
                    outputs=ext_style_dropdown
                )

                apply_button = ToolButton(
                    value=apply_style_symbol,
                    elem_id="extended_style_apply",
                )
                apply_button.click(
                    fn=apply_usecase.apply_ext_style,
                    _js='apply_extended_style',
                    inputs=[ext_style_dropdown],
                    outputs=[self.pos_prompt_component,
                             self.neg_prompt_component,
                             self.txt2img_width_component,
                             self.txt2img_height_component,
                             ]
                )
                refresh_button = ToolButton(
                    value=refresh_symbol,
                    elem_id="extended_style_refresh",
                )
                refresh_button.click(
                    fn=ext_style_service.refresh,
                    inputs=None,
                    outputs=ext_style_dropdown
                )

            with gr.Accordion('Save', open=False):
                with gr.Row():
                    save_style_button = ToolButton(
                        value=save_style_symbol,
                        elem_id="extended_style_create",
                    )
                    save_style_button.click(
                        fn=save_usecase.save,
                        _js="ask_for_extended_style_name",
                        # Have to pass empty dummy component here, because the JavaScript and Python function have to accept
                        # the same number of parameters, but we only know the style-name after the JavaScript prompt
                        inputs=[self.dummy_component, self.pos_prompt_component, self.neg_prompt_component,
                                self.txt2img_width_component, self.txt2img_height_component,
                                ],
                        outputs=ext_style_dropdown,
                    )
