
class IconPickerWidget {
    constructor(querySelector, value) {
        this.container = document.querySelector(querySelector + "__wrapper");

        this.input = this.container.querySelector(querySelector);
        this.inputDisplay = this.container.querySelector(querySelector + "__display");
        this.selectBox = this.container.querySelector(querySelector + "__select");

        this.selectItems = this.container.querySelectorAll(".icon-picker-list .icon-picker-select-item");
        this.setup();
        this.setState(value);
    }

    setup() {

        for (let i = 0; i < this.selectItems.length; i++) {
            const item = this.selectItems[i];
            const label = item.querySelector(".icon-picker-select-item-label");
            item.addEventListener('click', function(evt) {
                this.setState({
                    value: item.dataset.value,
                    label: label.innerHTML.trim()
                });
            }.bind(this));
        }
    }

    setState(data) {
        if (data === null) {
            data = {
                value: "",
                label: ""
            }
        } else if (data instanceof String || typeof data === "string") {
            let element = this.container.querySelector(`.icon-picker-select-item[data-value="${data}"]`);
            if (element) {
                const label = element.querySelector(".icon-picker-select-item-label");
                data = {
                    value: data,
                    label: label.innerHTML.trim()
                }
            }
        }
        this.input.value = data.value;
        this.inputDisplay.value = data.label;
    }

    getState() {
        return this.input.value;
    }

    getValue() {
        return this.getState();
    }

    focus() {
        this.input.focus();
    }
}