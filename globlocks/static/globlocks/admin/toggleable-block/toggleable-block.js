class ShowableBlockButton {
    constructor(def, block, settings, opts) {
        this.def = def;
        this.blockContainer = block.container[0];
        this.block = block;
        this.settings = settings;
        this.opts = opts || {};
        this._on = {
            show: [],
            hide: [],
            focus: [],
            blur: [],
        };
        this.element = this.render();
    }

    render() {
    
    }

    getState() {
        return true;
    }

    execFuncs(which) {
        this._on[which].forEach((cb) => {
            cb();
        });
    }

    bindTo(opts) {
        const {

            element     = this.element,
            premonition = () => true,
            eventName   = 'click',
            always      = null,
            ifTrue      = null,
            ifFalse     = null,

        } = opts;
        
        element.addEventListener(eventName, (e) => {
            let isTrue = premonition(e);
            if (always) {
                always(isTrue, e);
            }
            if (isTrue) {
                if (ifTrue) {
                    ifTrue(e);
                }
            } else {
                if (ifFalse) {
                    ifFalse(e);
                }
            }
        });
    }

    on(which, cb) {
        this._on[which].push(cb);
    }

    show() {
        this.execFuncs('show');
        this.blockContainer.classList.remove('globlocks-showable-block-hidden');
    }

    hide() {
        this.execFuncs('hide');
        this.blockContainer.classList.add('globlocks-showable-block-hidden');
    }

    focus() {
        this.execFuncs('focus');
    }

    blur() {
        this.execFuncs('blur');
    }
}



class ToggleableBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );

        const settings = block.childBlocks.settings;
        const buttonWrapper = document.createElement('div');
        buttonWrapper.classList.add('globlocks-showable-block-buttons');
        block.container[0].appendChild(buttonWrapper);
        block.showableButtons = {};

        const keys = Object.keys(this.meta.buttons);
        for (let i = 0; i < keys.length; i++) {
            const key = keys[i];
            const btnOpts = this.meta.buttons[key];
            const buttonClass = window.globlocks.showableBlockButtons["registry"][key];
            const button = new buttonClass(this, block, settings, btnOpts);
            block.showableButtons[key] = button;
            buttonWrapper.appendChild(button.element);
        }

        const container = block.container[0];
        container.classList.add('globlocks-showable-block');

        let isShown = true;
        for (let i = 0; i < keys.length; i++) {
            let button = block.showableButtons[keys[i]];
            if (!button.getState()) {
                isShown = false;
            }

            button.on('focus', () => {
                for (let j = 0; j < keys.length; j++) {
                    let buttonKey = keys[j];
                    if (buttonKey !== keys[i]) {
                        block.showableButtons[buttonKey].blur();
                    }
                }
            });
        }

        this.updateState(isShown, block, settings);

        return block;
    }

    updateState(isShown, block, settings, button=null) {
        if (isShown || button == null) {
            block.hiddenBy = [];
        } else {
            block.hiddenBy = [button];
        }
        const keys = Object.keys(block.showableButtons);
        for (let i = 0; i < keys.length; i++) {
            let buttonKey = keys[i];
            let cmpBtn = block.showableButtons[buttonKey];
            
            if (button == null || button !== null && button !== cmpBtn) {
                let state = cmpBtn.getState();
                isShown = isShown && state;
                if (!state) {
                    block.hiddenBy.push(cmpBtn);
                }
            } 
        }

        // if (block.shownState !== isShown) {
            if (isShown) {
                this.showBlock(block, settings);
            } else {
                this.hideBlock(block, settings);
            }
            block.shownState = isShown;
        // }
    }

    showBlock(block) {
        const container = block.container[0];
        container.classList.remove('globlocks-showable-block-hidden');
        const keys = Object.keys(block.showableButtons);
        for (let i = 0; i < keys.length; i++) {
            let buttonKey = keys[i];
            let button = block.showableButtons[buttonKey];
            button.show();
        }
    }

    hideBlock(block) {
        const container = block.container[0];
        container.classList.add('globlocks-showable-block-hidden');
        const keys = Object.keys(block.showableButtons);
        for (let i = 0; i < keys.length; i++) {
            let buttonKey = keys[i];
            let button = block.showableButtons[buttonKey];
            button.hide();
        }
    }

    replaceText(block, text) {
        return text.replace('{label}', block.getTextLabel());
    }
}

window.telepath.register('globlocks.blocks.ToggleShowableBlock', ToggleableBlockDefinition);


if (!window.globlocks) {
    window.globlocks = {};
}

if (!window.globlocks.showableBlockButtons) {
    window.globlocks.showableBlockButtons = {};
}

window.globlocks.showableBlockButtons['Base'] = ShowableBlockButton;
window.globlocks.showableBlockButtons["registry"] = {}
window.globlocks.registerShowableBlockButtons = function (buttons) {
    if (buttons instanceof Array) {
        const name = buttons[0];
        buttons = buttons[1];
        window.globlocks.showableBlockButtons["registry"][name] = buttons;
        return;
    }

    const keys = Object.keys(buttons);
    for (let i = 0; i < keys.length; i++) {
        const key = keys[i];
        window.globlocks.showableBlockButtons["registry"][key] = buttons[key];
    }
}
