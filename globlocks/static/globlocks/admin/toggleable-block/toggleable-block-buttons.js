const globlocksShowableBlockGetShownInput = function (settings) {
    const shownObj = settings.childBlocks.is_shown;
    const shownInputId = shownObj.idForLabel;
    const shownInput = document.getElementById(shownInputId);
    return {
        shownInput: shownInput,
        shownObj: shownObj,
    };
}

const svgIcon = (iconName, options) => {
    let svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute('width', '16');
    svg.setAttribute('height', '16');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.classList.add('icon', 'icon-' + iconName);
    let use = document.createElementNS("http://www.w3.org/2000/svg", "use");
    use.setAttribute('href', `#icon-${iconName}`);
    svg.appendChild(use);

    for (let key in options) {
        svg.setAttribute(key, options[key]);
    }

    return svg;
}

function wagtailButton(opts) {
    const {
        text,
        icon = null,
        className = null,
        type = 'button',
    } = opts;

    if (className && !Array.isArray(className)) {
        throw new Error('className must be an array');
    }

    if (className == null) {
        className = [];
    }

    const btn = document.createElement('button');
    btn.type = type;

    btn.classList.add(
        'button',
        'button-small',
    );

    btn.setIcon = (icon) => {
        if (btn.svgIcon) {
            btn.removeChild(btn.svgIcon);
        }

        if (!button.classList.contains('button--icon')) {
            btn.classList.add(
                'bicolor',
                'button--icon',
            )
        }

        let svg = svgIcon(icon);
        let span = document.createElement('span');
        span.classList.add('icon-wrapper');
        span.appendChild(svg);
        btn.appendChild(span);
        btn.svgIcon = svg;
        return svg;
    }

    if (icon) {
        btn.setIcon(icon);
    }

    if (className) {
        btn.classList.add(...className);
    }

    btn.appendChild(document.createTextNode(text));
    return btn;
}


class ToggleableBlockIsShownButton extends window.globlocks.showableBlockButtons.Base {
    constructor(def, block, settings, opts) {
        super(def, block, settings, opts);

        const {
            shownInput,
            shownObj,
        } = globlocksShowableBlockGetShownInput(settings);
        this.shownInput = shownInput;
        this.shownObj = shownObj;
        this.shownInput.addEventListener('change', (e) => {
            this.def.updateState(
                this.shownInput.checked,
                this.block,
                this.settings,
                this,
            )
        });
        
        const childBlockKeys = Object.keys(settings.childBlocks);
        if (childBlockKeys.length > 1) {
            let container = $(this.shownObj.element).closest('[data-contentpath]');
            container.css('display', 'none');
        }
    }

    getState() {
        return this.shownInput.checked;
    }

    render() {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.addEventListener('click', (e) => {
            if (this.block.hiddenBy.length > 0 && !(this.block.hiddenBy.includes(this))) {
                return;
            }
            this.focus();
            const changeEvent = new Event('change');
            this.shownInput.checked = !this.shownInput.checked;
            this.shownInput.dispatchEvent(changeEvent);
        });
        btn.classList.add(
            'globlocks-showable-block-button',
        )

        return btn;
    }
    
    show() {
        this.element.innerText = this.opts.translations.hideText;

        this.element.classList.remove('warning');
        this.element.classList.remove('danger');
        this.element.classList.add('success');
        // this.shownInput.checked = true;
    }

    hide() {
        this.element.innerText = this.opts.translations.showText;

        this.element.classList.remove('success');
        this.element.classList.remove('warning');
        this.element.classList.remove('danger');
        if (this.block.hiddenBy.length > 1 || !this.block.hiddenBy.includes(this)) {
            this.element.classList.add('danger');
        } else {
            this.element.classList.add('warning');
        }
    }
}


class DateFromToBaseButton extends window.globlocks.showableBlockButtons.Base {

    constructor(def, block, settings, opts) {
        super(def, block, settings, opts);
        this.dateInput = this.getDateInput();
        this.date = null;

        if (this.dateInput && this.dateInput.value) {
            this.date = new Date(this.dateInput.value);
        }

    }

    getText() {
        return this.def.replaceText(this.block, this.opts.label);
    }

    getState() {
        if (this.date === null) {
            return true;
        }

        return !this.op(this.date, new Date());
    }

    render() {
        const wrapper = document.createElement('div');
        wrapper.classList.add('globlocks-showable-block-buttons-menu');

        this.svgOpen = svgIcon('lock-open', {style: {display: 'none'}});
        this.svgClosed = svgIcon('lock', {style: {display: 'none'}});

        this.button = document.createElement('button');
        this.button.appendChild(this.svgOpen);
        this.button.appendChild(this.svgClosed);
        this.button.type = 'button';
        this.button.appendChild(
            document.createTextNode(this.getText())
        );
        
        this.button.classList.add(
            'globlocks-showable-block-button',
            'globlocks-showable-block-buttons-menu-toggle',
        )

        this.bindTo({
            element: this.button,
            premonition: (e) => {
                return inputWrapper.style.display === 'block'
            },
            eventName: 'click',
            ifTrue: this.blur.bind(this),
            ifFalse: this.focus.bind(this),
        });

        const inputWrapper = document.createElement('div');
        inputWrapper.classList.add(
            'globlocks-showable-block-buttons-menu-content',
        );
        inputWrapper.style.display = 'none';
        this.dateInput = this.getDateInput();
        this.dateInput.setAttribute('autocomplete', 'off')
        this.dateInput.addEventListener('change', (e) => {
            this.date = new Date(this.dateInput.value);
            this.def.updateState(
                this.getState(),
                this.block,
                this.settings,
                this,
            );
        });
        inputWrapper.appendChild(this.dateInput);

        this.on('focus', () => {
            inputWrapper.style.display = 'block';
            this.dateInput.focus();
        })
    
        this.on('blur', () => {
            inputWrapper.style.display = 'none';
        })

        wrapper.appendChild(this.button);
        wrapper.appendChild(inputWrapper);
        return wrapper;
    }

    show() {
        if (!this.getState()) {
            this.button.classList.remove('success');
            this.button.classList.add('danger');
            this.svgOpen.style.display = 'none';
            this.svgClosed.style.display = 'inline-block';
        } else {
            this.button.classList.remove('danger');
            this.button.classList.add('success');
            this.svgOpen.style.display = 'inline-block';
            this.svgClosed.style.display = 'none';
        }
    }

    hide() {
        if (this.getState()) {
            this.button.classList.remove('danger');
            this.button.classList.add('success');
            this.svgOpen.style.display = 'inline-block';
            this.svgClosed.style.display = 'none';
        } else {
            this.button.classList.remove('success');
            this.button.classList.add('danger');
            this.svgOpen.style.display = 'none';
            this.svgClosed.style.display = 'inline-block';
        }
    }
}


class DateFromButton extends DateFromToBaseButton {
    constructor(def, block, settings, opts) {
        super(def, block, settings, opts);
    }

    op(a, b) {
        return a > b;
    }
    
    getDateInput() {
        if (this.dateInput) {
            return this.dateInput;
        }
        const inputDef = this.settings.childBlocks.hide_before_date;
        let container = $(inputDef.element).closest('[data-contentpath]');
        container.css('display', 'none');

        const inputId = inputDef.idForLabel;
        const input = document.getElementById(inputId);
        return input;
    }
}

class DateToButton extends DateFromToBaseButton {
    constructor(def, block, settings, opts) {
        super(def, block, settings, opts);
    }

    op(a, b) {
        return a < b;
    }

    getDateInput() {
        if (this.dateInput) {
            return this.dateInput;
        }
        const inputDef = this.settings.childBlocks.hide_after_date;
        let container = $(inputDef.element).closest('[data-contentpath]');
        container.css('display', 'none');

        const inputId = inputDef.idForLabel;
        const input = document.getElementById(inputId);
        return input;
    }
}


window.globlocks.registerShowableBlockButtons({
    hide_before_date: DateFromButton,
    hide_after_date: DateToButton,
    is_shown: ToggleableBlockIsShownButton,
});