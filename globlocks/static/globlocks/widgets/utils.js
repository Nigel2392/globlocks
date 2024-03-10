

function getTargetFromPython(wagtailPanel, target) {
    let targetPanel = $(wagtailPanel);
    if (!targetPanel) {
        throw new Error('ToolbarWidget requires a target panel');
    }
    let targetWrapper = targetPanel.find(`div[data-contentpath="${target}"]`);
    if (!targetWrapper) {
        throw new Error('ToolbarWidget requires a target wrapper');
    }
    let inputs = targetWrapper.find('input');
    for (let j = 0; j < inputs.length; j++) {
        let input = inputs[j];
        let inputId = input.id;
        if (inputId && inputId.length >= target.length && inputId.substring(inputId.length - target.length) === target) {
            return input;
        }
    }
    return null;
}

