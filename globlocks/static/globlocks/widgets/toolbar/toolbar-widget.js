function getToolbarWidgetTool(tool) {
    if (tool) {
        if (window.toolbarWidgetTools && tool in window.toolbarWidgetTools) {
            return window.toolbarWidgetTools[tool];
        } else if (tool in TOOLBAR_WIDGETS) {
            return TOOLBAR_WIDGETS[tool];
        }
    }
    return null;
}


function registerToolbarWidgetTool(toolObject) {
    if (!window.toolbarWidgetTools) {
        window.toolbarWidgetTools = {};
    }
    window.toolbarWidgetTools[tool.toolType] = toolObject;
}


class ToolbarTool {
    constructor(toolType) {
        if (!toolType) {
            throw new Error('ToolbarWidgetTool requires a toolType');
        }
        this.toolType = toolType;
    }

    get group() {
        return null;
    }

    isActive(value) {
        return !!value;
    }

    initialize(toolbar, button, target, value = null) {
        this.toolbar = toolbar;
        this.button = button;
        this.target = target;
        this.value = value;
    }

    execute(target, groups = null) {
        if (groups) {
            for (let j = 0; j < groups.length; j++) {
                let groupTool = groups[j];
                if (groupTool !== this) {
                    groupTool.resetState(this.target);
                    groupTool.button.classList.remove('active');
                }
            }
        }

        if (this.button.classList.contains('active')) {
            this.resetState(target);
            this.button.classList.remove('active');
         } else {
             this.setState(target);
             this.button.classList.add('active');
         }
    }

    setState(target) {
        // Do nothing
    }

    resetState(target) {
        // Do nothing
    }
}


class StyleToolbarWidgetTool extends ToolbarTool {

    constructor(toolType, styleAttribute, styleValue = null, group = null) {
        super(toolType);
        if (!styleValue) {
            throw new Error('StyleToolbarWidgetTool requires a styleValue');
        }

        if (typeof styleValue === 'string') {
            styleValue = styleValue.split(' ');
        }

        this.styleAttribute = styleAttribute;
        this.styleValue = styleValue;
        this._group = group;
    }

    get group() {
        return this._group;
    }

    getState() {
        let styleValue = this.target.style[this.styleAttribute];
        if (styleValue) {
            styleValue = styleValue.split(' ');
        }
        return styleValue;
    }

    setState(target) {
        let styleValue = this.getState() || [];
        for (let i = 0; i < this.styleValue.length; i++) {
            let value = this.styleValue[i];
            if (styleValue.indexOf(value) === -1) {
                styleValue.push(value);
            }
        }
        target.style[this.styleAttribute] = styleValue.join(' ');
    }

    resetState(target) {
        let styleValue = this.getState() || [];
        for (let i = 0; i < this.styleValue.length; i++) {
            let value = this.styleValue[i];
            if (styleValue.indexOf(value) !== -1) {
                styleValue.splice(styleValue.indexOf(value), 1);
            }
        }
        target.style[this.styleAttribute] = styleValue.join(' ');
    }

    isActive(value) {
        if (value) {
            if (typeof value === typeof []) {
                if (typeof this.styleValue === typeof []) {
                    for (let i = 0; i < value.length; i++) {
                        if (this.styleValue.indexOf(value[i]) !== -1) {
                            return true;
                        }
                    }
                } else {
                    return this.styleValue.indexOf(value) !== -1;
                }
            } else {
                if (typeof this.styleValue === typeof []) {
                    return this.styleValue.indexOf(value) !== -1;
                } else {
                    return this.styleValue === value;
                }
            }
        } 
        return false;
    }
}

const _HEADINGS = {
    'HEADING_1': {
        'fontSize': '3em',
        'heading': 'h1',
    },
    'HEADING_2': {
        'fontSize': '2.5em',
        'heading': 'h2',
    },
    'HEADING_3': {
        'fontSize': '2em',
        'heading': 'h3',
    },
    'HEADING_4': {
        'fontSize': '1.5em',
        'heading': 'h4',
    },
    'HEADING_5': {
        'fontSize': '1.25em',
        'heading': 'h5',
    },
    'HEADING_6': {
        'fontSize': '1em',
        'heading': 'h6',
    },
}

class HeadingToolbarWidgetTool extends ToolbarTool {
    constructor(toolType) {
        super(toolType);
        if (!(toolType in _HEADINGS)) {
            throw new Error('HeadingToolbarWidgetTool requires a valid toolType');
        }
        
        this._heading = _HEADINGS[toolType];
    }

    get group() {
        return 'heading';
    }

    isActive(value) {
        return value === this._heading.heading;
    }

    getState() {
        return this.target.dataset[this._heading.heading];
    }

    setState(target) {
        target.dataset[this._heading.heading] = this._heading.heading;
        target.style.fontSize = this._heading.fontSize;
    }

    resetState(target) {
        delete target.dataset[this._heading.heading];
        target.style.fontSize = '';
    }
}


class ColorToolbarWidgetTool extends ToolbarTool {
    constructor(toolType, attribute) {
        super(toolType);
        this.attribute = attribute;
    }

    isActive(value) {
        console.log('isActive: ', value);
        return !!value;
    }

    initialize(toolbar, button, target, value = null) {
        super.initialize(toolbar, button, target, value);
        if (!("Pickr" in window)) {
            throw new Error('ColorToolbarWidgetTool requires Pickr - did you load pickr.js?');
        }
        this.button = button;
        this.target = target;
        this.pickr = Pickr.create({
            el: this.button,
            useAsButton: true,
            swatches: [
                'rgba(244, 67, 54, 1)',
                'rgba(233, 30, 99, 0.95)',
                'rgba(156, 39, 176, 0.9)',
                'rgba(103, 58, 183, 0.85)',
                'rgba(63, 81, 181, 0.8)',
                'rgba(33, 150, 243, 0.75)',
                'rgba(3, 169, 244, 0.7)',
                'rgba(0, 188, 212, 0.7)',
                'rgba(0, 150, 136, 0.75)',
                'rgba(76, 175, 80, 0.8)',
                'rgba(139, 195, 74, 0.85)',
                'rgba(205, 220, 57, 0.9)',
                'rgba(255, 235, 59, 0.95)',
                'rgba(255, 193, 7, 1)'
            ],
        
            components: {
            
                // Main components
                preview: true,
                opacity: true,
                hue: true,
            
                // Input / output Options
                interaction: {
                    hex: true,
                    rgba: true,
                    hsla: true,
                    hsva: true,
                    cmyk: true,
                    input: true,
                    clear: true,
                    save: true
                }
            }
        });
        this.pickr.on('save', (color, instance) => {
            if (color) {
                this.value = color.toRGBA().toString(1);
                this.setState(this.target);
            } else {
                this.resetState(this.target);
            }
        });
        if (this.value) {
            this.pickr.on('init', (color, instance) => {
                this.setState(this.target);
            });
        }
        this.pickr.on('clear', (color, instance) => {
            console.log('clear');
            this.resetState(this.target);
        });
    }

    execute(target, group = null) {
        if (target.dataset[this.attribute]) {
            this.button.classList.add('active');
        } else {
            this.button.classList.remove('active');
        }
    }

    getState() {
        return this.target.dataset[this.attribute]
    }

    setState(target) {
        target.dataset[this.attribute] = this.value;
        target.style[this.attribute] = this.value;
        this.button.classList.add('active');

    }

    resetState(target) {
        this.value = null;
        delete target.dataset[this.attribute];
        target.style[this.attribute] = '';
        this.button.classList.remove('active');
    }
}


const TOOLBAR_WIDGETS = {
    BOLD: new StyleToolbarWidgetTool("BOLD", 'fontWeight', 'bold'),
    ITALIC: new StyleToolbarWidgetTool("ITALIC", 'fontStyle', 'italic'),
    UNDERLINE: new StyleToolbarWidgetTool("UNDERLINE", 'textDecoration', 'underline'),
    STRIKETHROUGH: new StyleToolbarWidgetTool("STRIKETHROUGH", 'textDecoration', 'line-through'),
    JUSTIFY_LEFT: new StyleToolbarWidgetTool("JUSTIFY_LEFT", 'textAlign', 'left', "text-align"),
    JUSTIFY_CENTER: new StyleToolbarWidgetTool("JUSTIFY_CENTER", 'textAlign', 'center', "text-align"),
    JUSTIFY_RIGHT: new StyleToolbarWidgetTool("JUSTIFY_RIGHT", 'textAlign', 'right', "text-align"),

    HEADING_1: new HeadingToolbarWidgetTool("HEADING_1", 'fontSize', '2em', "heading"),
    HEADING_2: new HeadingToolbarWidgetTool("HEADING_2", 'fontSize', '1.5em', "heading"),
    HEADING_3: new HeadingToolbarWidgetTool("HEADING_3", 'fontSize', '1.17em', "heading"),
    HEADING_4: new HeadingToolbarWidgetTool("HEADING_4", 'fontSize', '1em', "heading"),
    HEADING_5: new HeadingToolbarWidgetTool("HEADING_5", 'fontSize', '0.83em', "heading"),
    HEADING_6: new HeadingToolbarWidgetTool("HEADING_6", 'fontSize', '0.67em', "heading"),

    COLOR: new ColorToolbarWidgetTool("COLOR", 'color'),
    BACKGROUND_COLOR: new ColorToolbarWidgetTool("BACKGROUND_COLOR", 'backgroundColor'),
}
/**
 * A toolbar widget
 * 
 * @param {string} querySelector - The query selector for the toolbar widget
 * @param {object} value - The initial value of the toolbar widget
 * @param {string} target - The target input id
 * @param {array} tools - The tools to register
 */
class ToolbarWidget {
    constructor(querySelector, target = null, tools = null) {
        if (tools === null) {
            tools = Object.keys(TOOLBAR_WIDGETS);
        }

        if (target === null) {
            throw new Error('ToolbarWidget requires a target');
        }

        /** @type {HTMLElement} */
        this.wrapper = document.querySelector(`#${querySelector}`);
        /** @type {HTMLInputElement} */
        this.input = this.wrapper.querySelector(`#${querySelector}-input`);
        /** @type {HTMLElement} */
        this.toolbar = this.wrapper.querySelector(`#${querySelector}-toolbar`);
        /** @type {NodeList} */
        this.toolbarButtons = this.toolbar.querySelectorAll('.toolbar-button');
        /** @type {HTMLElement} */
        this.target = getTargetFromPython($(this.wrapper).closest(`.w-panel`), target);
        if (!this.target) {
            throw new Error('ToolbarWidget requires a target input: ' + target);
        }

        let value = null;
        if (this.input.value) {
            value = JSON.parse($(this.input).val());
        }

        if (!value) {
            value = {};
        }

        /** @type {Array<string>} */
        this.registeredTools = tools;
        /** @type {Object<string, ToolbarTool>} */
        this._registeredToolObjects = {};
        /** @type {Object<string, Array<ToolbarTool>>} */
        this._toolGroups = {};

        for (let i = 0; i < this.registeredTools.length; i++) {

            let tool = this.registeredTools[i];
            let toolObj = getToolbarWidgetTool(tool);
            if (!toolObj) {
                throw new Error(`ToolbarWidget tool ${tool} not found`);
            }
            toolObj = Object.assign(Object.create(Object.getPrototypeOf(toolObj)), toolObj);

            this._registeredToolObjects[tool] = toolObj;

            if (toolObj.group) {
                if (!(toolObj.group in this._toolGroups)) {
                    this._toolGroups[toolObj.group] = [];
                }
                this._toolGroups[toolObj.group].push(toolObj);
            }
        }

        for (let i = 0; i < this.toolbarButtons.length; i++) {
            /*
                A button can have multiple tools, so we need to loop through each tool
                Example of a button :
                
                <button class="toolbar-input" data-tool="bold" data-tool-group="text" type="button">
                    <i class="fa fa-bold"></i>
                </button>
            */
            const button = this.toolbarButtons[i];
            const tool = button.getAttribute('data-tool');
            const toolObject = this._registeredToolObjects[tool];
            if (!toolObject) {
                throw new Error(`ToolbarWidget tool ${tool} not found in: ${this.registeredTools}`);
            }

            button.addEventListener('click', function(e) {
                this.updateGroup(toolObject);
            }.bind(this));

            if (tool in value) {
                toolObject.initialize(this, button, this.target, value[tool]);
            } else {
                toolObject.initialize(this, button, this.target, {});
            }
            
            if (toolObject.isActive(value[tool])) {
                toolObject.setState(this.target);
                toolObject.button.classList.add('active');
            }
        }
    }

    updateState() {
        this.setState(this.getState(), true);
    }

    updateGroup(toolObject) {
        let toolGroup = toolObject.group;
        let groupObject = this._toolGroups[toolGroup];

        // Let the tool decide how to handle it.
        toolObject.execute(this.target, groupObject);

        this.updateState();
    }

    setTools(value) {
        for (let i = 0; i < this.registeredTools.length; i++) {
            let tool = this.registeredTools[i];
            let toolObject = this._registeredToolObjects[tool];
            if (!toolObject) {
                throw new Error(`ToolbarWidget tool ${tool} not found`);
            }
            if (tool in value && value[tool]) {
                toolObject.setState(this.target);
                toolObject.button.classList.add('active');
            } else {
                toolObject.resetState(this.target);
                toolObject.button.classList.remove('active');
            }
        }
    }

    setState(value, skipTools = false) {
        if (!value) {
            return;
        }
        if (!skipTools) {
            this.setTools(value);
        }
        this.input.value = JSON.stringify(value);
    }

    getState() {
        let state = {};
        for (let i = 0; i < this.registeredTools.length; i++) {
            let tool = this.registeredTools[i];
            let toolObject = this._registeredToolObjects[tool];
            if (!toolObject) {
                throw new Error(`ToolbarWidget tool ${tool} not found`);
            }
            let toolState = toolObject.getState();
            if (toolState) {
                state[tool] = toolState;
            }
        }
        return state;
    }

    getValue() {
        return this.getState();
    }

    focus() {
        this.toolbar.focus();
    }

    disconnect() {
        // Do nothing
    }
}