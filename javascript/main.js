function ask_for_extended_style_name(_, prompt_text, negative_prompt_text, width, height) {
    const name_ = prompt('Style name:');
    return [name_, prompt_text, negative_prompt_text, width, height];
}

function apply_extended_style(style_name) {
    regexp = /\(([^)]*),([^)]*)\)$/g
    result = regexp.exec(style_name)
    model_name = result[1]
    vae_name = result[2]

    const sd_model = gradioApp().querySelector("#setting_sd_model_checkpoint" + " input");
    const vae = gradioApp().querySelector("#setting_sd_vae" + " input");
    sd_model.value = model_name
    vae.value = vae_name
    return [style_name]
}

