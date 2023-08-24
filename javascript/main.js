function ask_for_extended_style_name(str) {
    var name_ = prompt('Style name:');
    return [name_];
}


// Sync the value of the selected model from the main SD model list to the model list of this extension
function setSelectValue(selectPreviewModelElement, selectSDModelElement) {
    // Check if the element exists, is not null, and its value is different than the SD model checkpoint
    if (typeof selectPreviewModelElement != "undefined" && selectPreviewModelElement != null &&
        selectPreviewModelElement.value != selectSDModelElement.value) {
        // Set the value of the preview model list to the value of the SD model checkpoint
        selectPreviewModelElement.value = selectSDModelElement.value;
        // Get the options of the preview model list as an array
        const options = Array.from(selectPreviewModelElement.options);
        // Find the option in the array that has the same text as the SD model checkpoint value
        const optionToSelect = options.find(item => item.text == selectSDModelElement.value);
        // Check if the option was found and is not null
        if (typeof optionToSelect != "undefined" && optionToSelect != null) {
            // Mark the option as selected
            optionToSelect.selected = true;
            // Dispatch a change event on the preview model list
            selectPreviewModelElement.dispatchEvent(new Event('change'));
        }
    }
}