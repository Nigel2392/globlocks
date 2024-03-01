class RangeSlider {
    constructor(querySelector, value=null, unit = "") {
        this.querySelector = querySelector;
        this.input = document.querySelector("#"+querySelector);

        if (!this.input) {
            console.error(`Could not find element with id ${querySelector}`);
            return;
        }

        this.previewText = document.querySelector(`#${querySelector}-preview-text`);
        this.input.classList.add("range-slider-converted");
        this.value = null;
        this.unit = unit;

        if (this.value == "None") {
            this.value = null;
        }

        this.setState(value);
        this.listen();
    }

    setState(value) {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        this.value = value || 0;
        this.input.value = this.value
        this.updatePreviewText();
    }

    updatePreviewText() {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        this.previewText.innerHTML = `${this.value}${this.unit}`;
    }

    listen() {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        this.input.oninput = function(e) {
            this.setState(e.target.value);
        }.bind(this);
    }

    getState() {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        return this.value;
    }

    getValue() {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        return this.value;
    }

    focus() {
        if (!this.input) {
            console.error("RangeSlider is not initialized for element: " + this.querySelector);
            return;
        }
        this.input.focus();
    }
}