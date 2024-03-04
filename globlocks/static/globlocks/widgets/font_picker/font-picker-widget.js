
class FontPickerWidget {
    constructor(querySelector, value, unit = "em") {
        this.value = null;
        this.input = document.querySelector("#"+querySelector);
        this.select = document.querySelector(`#${querySelector}-picker`);
        this.previewText = document.querySelector(`#${querySelector}-preview-text`);
        this.sizeInput = document.querySelector(`#${querySelector}-size`);
        this.unit = unit;
        this.setup();
        this.listen();
        this.setState(value);
    }

    setup() {
        for (let i = 0; i < this.select.options.length; i++) {
            let option = this.select.options[i];
            let font = new FontFace(option.dataset.fontfamily, `url(${option.dataset.import})`);
            font.load().then(function(loaded_face) {
                document.fonts.add(loaded_face);
            }).catch(function(error) {
                console.error(error);
            });
            option.style.fontFamily = option.dataset.fontfamily;
        }
    }

    listen() {
        let fn = (e) => {
            let selectedOption = this.selectedOption();
            this.setState({
                name: selectedOption.dataset.fontfamily,
                path: e.target.value
            }, selectedOption);
        };
        fn.bind(this);
        this.select.addEventListener('change', fn);
        this.sizeInput.addEventListener('change', this.updatePreviewText.bind(this));
    }

    selectedOption() {
        let selectedIndex = this.select.selectedIndex;
        let selectedOption = this.select.options[selectedIndex];

        if (selectedOption == null) {
            selectedOption = this.select.options[0];
            this.select.selectedIndex = 0;
        }

        return selectedOption;
    }

    loadFont(selectedOption = null) {
        if (selectedOption == null) {
            selectedOption = this.selectedOption();
        }
        this.previewText.style.fontFamily = selectedOption.dataset.fontfamily;
        this.select.style.fontFamily = selectedOption.dataset.fontfamily;
    }

    updatePreviewText() {
        this.previewText.style.fontSize = `${this.sizeInput.value}${this.unit}`;;
        this.previewText.style.fontFamily = this.value.name;
    }


    setState(value, selectedOption=null) {
        if (value == null) {
            let selected = selectedOption || this.selectedOption();
            value = {
                name: selected.dataset.fontfamily,
                path: selected.value,
                size: this.sizeInput.value,
                unit: this.unit
            }
        }
        this.value = value;
        this.sizeInput.value = value.size || this.sizeInput.value || 1.0;
        this.input.value = JSON.stringify(value);
        this.select.value = value.path;
        this.updatePreviewText();
        this.loadFont(selectedOption);
    }

    getState() {
        let selected = this.selectedOption();
        return {
            name: selected.dataset.fontfamily,
            path: selected.value,
            size: this.sizeInput.value
        };
    }

    getValue() {
        return JSON.stringify(this.getState());
    }

    focus() {
        this.select.focus();
    }
}