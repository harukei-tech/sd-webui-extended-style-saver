function ask_for_extended_style_name(_, prompt_text, negative_prompt_text, width, height, txt2img_width_component, txt2img_height_component) {
    const name_ = prompt('Style name:');
    if (name_ === null) {
        throw '';
    }
    return [name_, prompt_text, negative_prompt_text, width, height, txt2img_width_component, txt2img_height_component]
}

function apply_extended_style(style_name) {
    regexp = /(.*)\(([^)]*),([^)]*),([^)]*)\)$/g
    result = regexp.exec(style_name)
    ext_style_name = result[1].trim()
    model_name = result[2].trim()
    vae_name = result[3].trim()
    id = result[4].trim()

    const sd_model = gradioApp().querySelector("#setting_sd_model_checkpoint" + " input")
    const vae = gradioApp().querySelector("#setting_sd_vae" + " input")
    sd_model.value = model_name
    vae.value = vae_name

    return style_name
}

function confirm_extended_style_deletion(style_name) {
    regexp = /(.*)\(([^)]*),([^)]*),([^)]*)\)$/g
    result = regexp.exec(style_name)
    ext_style_name = result[1].trim()
    model_name = result[2].trim()
    vae_name = result[3].trim()
    id = result[4].trim()

    if (!confirm('Are you sure you want to delete the style "' + ext_style_name + '"?')) {
        throw ''
    }

    return id
}