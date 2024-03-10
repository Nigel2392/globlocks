class JustifyWidget {
    constructor(querySelector, value = null, targets = []) {
        this.targets = targets;
        this.radioSelect = document.querySelector(`#${querySelector}`);        
        this.radioSelectInputs = {};
        let inputs = this.radioSelect.querySelectorAll('input[type="radio"]');

        for (let i = 0; i < inputs.length; i++) {
            let input = inputs[i];
            this.radioSelectInputs[input.value] = input;
            input.addEventListener('change', (e) => {
                this.setState(e.target.value);
            });
        }

        if (value) {
            this.setState(value);
        }
    }

    updateTargetElements() {
        const keys = Object.keys(this.radioSelectInputs);
        for (let i = 0; i < this.targets.length; i++) {
            let target = this.targets[i];
            let targetPanel = $(this.radioSelect).closest(`.w-panel`);
            if (!targetPanel) {
                continue;
            }
            let targetWrapper = targetPanel.find(`div[data-contentpath="${target}"]`);
            if (!targetWrapper) {
                continue
            }
            let inputs = targetWrapper.find('input');
            for (let j = 0; j < inputs.length; j++) {
                let input = inputs[j];
                let inputId = input.id;
                if (inputId && inputId.length >= target.length && inputId.substring(inputId.length - target.length) === target) {
                    for (let k = 0; k < keys.length; k++) {
                        let key = keys[k];
                        if ($(input).hasClass(key)) {
                            $(input).removeClass(key);
                        }
                    }
                    const value = this.getValue();
                    $(input).addClass(value);
                }
            }
        }
    }

    setDefault() {
        let key = Object.keys(this.radioSelectInputs)[0]
        this.setState(this.radioSelectInputs[key].value);
    }

    setState(value) {
        if (!value) {
            this.setDefault();
            return;
        }
        this.value = value;
        this.radioSelectInputs[value].checked = true;
        this.updateTargetElements();
    }

    getState() {
        return this.value;
    }

    getValue() {
        let value = this.getState();
        if (!value) {
            this.setDefault()
        }
        return value;
    }

    focus() {
        this.radioSelect.focus();
    }

    disconnect() {
        // Do nothing
    }
}
