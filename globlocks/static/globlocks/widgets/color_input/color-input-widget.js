
function invertColor(hex) {
    return (Number(`0x1${hex}`) ^ 0xFFFFFF).toString(16).substr(1).toUpperCase()
}

class ColorInputWidget {
    constructor(id) {
        /*
        id = the ID of the HTML element where color input behaviour should be attached
        */
        this.textInput = document.getElementById(id);
        this.colorInput = document.getElementById(id + "-color-btn");

        this.textInput.addEventListener('change', this.handleUpdate.bind(this));

        this.pickr = Pickr.create({
            el: this.colorInput,
            theme: 'classic', // or 'monolith', or 'nano'
            useAsButton: true,
            default: this.textInput.value,
            defaultRepresentation: 'RGBA',
            swatches: [
                'rgba(244, 67, 54, 1)',
                'rgba(233, 30, 99, 1)',
                'rgba(156, 39, 176, 1)',
                'rgba(103, 58, 183, 1)',
                'rgba(63, 81, 181, 1)',
                'rgba(33, 150, 243, 1)',
                'rgba(3, 169, 244, 1)',
            ],
            components: {

                // Main components
                preview: true,
                opacity: true,
                hue: true,
            
                // Input / output Options
                interaction: {
                    //hex: true,
                    rgba: true,
                    //hsla: true,
                    //hsva: true,
                    cancel: true,
                    clear: true,
                    save: true
                }
            }
        })
        function savePickrColor(color, instance){
            const rep = this.pickr.getColorRepresentation();
            let formattedColor;
            if (rep == "RGBA") {
                formattedColor = color.toRGBA().toString(1);
            } else if (rep == "HSLA") {
                formattedColor = color.toHSLA().toString();
            } else if (rep == "HSVA") {
                formattedColor = color.toHSVA().toString();
            } else if (rep == "HEXA") {
                formattedColor = color.toHEXA().toString();
            }
            this.textInput.value = formattedColor;
            this.textInput.dispatchEvent(new Event('change', {
                was_manually_triggered: true
            }));
        }

        this.pickr.on('change', savePickrColor.bind(this));
        this.pickr.on('save', savePickrColor.bind(this));
        this.pickr.on('clear', (color, instance) => {
            this.textInput.value = "";
        });
        this.pickr.on('init', instance => {
            let hexColor = this.pickr.getColor().toHEXA().toString()
            hexColor = hexColor.substring(0, hexColor.length - 2)
            this.textInput.style.backgroundColor = hexColor;
            
            hexColor = hexColor.replace("#", "")
            hexColor = invertColor(hexColor)
            this.textInput.style.color = "#" + hexColor;
        })
    }
    handleUpdate(evt) {
        if (evt.was_manually_triggered) {
            return;
        }
        this.setState(evt.target.value);
    }

    setState(newState) {
        this.textInput.value = newState;
        this.pickr.setColor(newState, true);

        let hexColor = this.pickr.getColor().toHEXA().toString()
        if (hexColor.length > 7) {
            hexColor = hexColor.substring(0, hexColor.length - 2)
        }
        this.textInput.style.backgroundColor = hexColor;
        
        hexColor = hexColor.replace("#", "")
        hexColor = invertColor(hexColor)
        this.textInput.style.color = "#" + hexColor;
    }

    getState() {
        return this.textInput.value;
    }

    getValue() {
        return this.textInput.value;
    }

    focus() {
        this.textInput.focus();
    }
}
