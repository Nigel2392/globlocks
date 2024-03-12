function atobJSON(str) {
    try {
        data = atob(str);
    } catch (e) {
        throw new Error('Malformed base64 string');
    }
    try {
        data = JSON.parse(data);
    } catch (e) {
        throw new Error('Malformed JSON string');
    }
    return data;
}

class ToolbarController extends window.StimulusModule.Controller {
    static values = { 
        targets:            { type: String },
        tools:              { type: String },
        // object:              { default: {}, type: Object },
    };

    connect() {

        let targets = atobJSON(this.targetsValue);
        let tools = atobJSON(this.toolsValue);

        this.toolbar = new ToolbarWidget(
            this.element.id,
            targets,
            tools,
        );
    }

    disconnect() {
        this.toolbar.disconnect();
        this.toolbar = null;
    }
}

window.wagtail.app.register('toolbar-widget', ToolbarController);
