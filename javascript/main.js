function ask_for_extended_style_name(_, prompt_text, negative_prompt_text, width, height, txt2img_width_component, txt2img_height_component, controlnet_enebled, controlnet_model, controlnet_input_image, controlnet_generated_image) {
    const name_ = prompt('Style name:');
    if (name_ === null) {
        throw '';
    }
    return [name_, prompt_text, negative_prompt_text, width, height, txt2img_width_component, txt2img_height_component, controlnet_enebled, controlnet_model, controlnet_input_image, controlnet_generated_image]
}

function apply_extended_style(style_name) {
    regexp = /\(([^)]*),([^)]*)\)$/g
    result = regexp.exec(style_name)
    model_name = result[1]
    vae_name = result[2]

    const sd_model = gradioApp().querySelector("#setting_sd_model_checkpoint" + " input")
    const vae = gradioApp().querySelector("#setting_sd_vae" + " input")
    sd_model.value = model_name
    vae.value = vae_name

    const is_controlnete_opened = gradioApp().querySelector('#controlnet > .open')
    if (!is_controlnete_opened) {
        const accordion = gradioApp().querySelector('#controlnet > .label-wrap')
        if (accordion != null) {
            accordion.click()
        }
    }
    return style_name
}

