class JustifyWidget {
    constructor(querySelector, value = null, targets = []) {
        this.targets = targets;
        this.radioSelect = document.querySelector(`#${querySelector}`);        
        this.radioSelectInputs = {};
        let inputs = this.radioSelect.querySelectorAll('input[type="radio"]');

        console.log('JustifyWidget', this.radioSelect, inputs);

        for (let i = 0; i < inputs.length; i++) {
            let input = inputs[i];
            this.radioSelectInputs[input.value] = input;
            input.addEventListener('change', (e) => {
                this.setState(e.target.value);
            });
        }

        if (value) {
            this.setState(value);
        } else {
            this.setDefault();
        }
    }

    updateTargetElements() {
        const keys = Object.keys(this.radioSelectInputs);
        for (let i = 0; i < this.targets.length; i++) {
            let target = this.targets[i];
            let targetPanel = $(this.radioSelect).closest(`.w-panel`);
            if (!targetPanel) {
                console.error(`Target panel not found for target: ${target}`, this.radioSelect);
                continue;
            }
            let targetWrapper = targetPanel.find(`div[data-contentpath="${target}"]`);
            if (!targetWrapper) {
                console.error(`Target wrapper not found for target: ${target}`, this.targetPanel);
                continue
            }
            let inputs = [
                ...targetWrapper.find('input'),
                ...targetWrapper.find('textarea'),
                ...targetWrapper.find('.Draftail-Editor'),
            ];

            let $targetWrapper = $(targetWrapper);
            const value = this.getValue();
            for (let j = 0; j < keys.length; j++) {
                let key = keys[j];
                $targetWrapper.removeClass(key);
            }

            $targetWrapper.addClass(value);

            for (let j = 0; j < inputs.length; j++) {
                let input = inputs[j];
                let $input = $(input);
                let inputId = input.id;
                if (inputId && inputId.length >= target.length && inputId.substring(inputId.length - target.length) === target) {
                    for (let k = 0; k < keys.length; k++) {
                        let key = keys[k];
                        if ($input.hasClass(key)) {
                            $input.removeClass(key);
                        }
                    }
                    $input.addClass(value);
                } else if ($input.hasClass('Draftail-Editor')) {
                    for (let k = 0; k < keys.length; k++) {
                        let key = keys[k];
                        if ($input.hasClass(key)) {
                            $input.removeClass(key);
                        }
                    }
                    $input.addClass(value);
                }
            }
            if (inputs.length === 0) {
                console.error(`No inputs found for target: ${target}`, targetWrapper);
            }
        }
    }

    setDefault() {
        if (!this.radioSelectInputs) {
            return;
        }
        const keys = Object.keys(this.radioSelectInputs)
        for (let i = 0; i < keys.length; i++) {
            let key = keys[i];
            if (!key) {
                continue;
            }
            if (this.radioSelectInputs[key].checked) {
                this.setState(key, true);
                return;
            }
        }
        const key = keys[0]
        this.setState(this.radioSelectInputs[key].value, true);
    }

    setState(value, isFromDefault = false) {
        if (!value && !isFromDefault) {
            this.setDefault();
            return;
        }
        this.value = value;
        this.radioSelectInputs[value].checked = true;
        this.updateTargetElements();
    }

    getState() {
        for (let i = 0; i < this.radioSelectInputs.length; i++) {
            let input = this.radioSelectInputs[i];
            if (input.checked) {
                return input.value;
            }
        }
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
