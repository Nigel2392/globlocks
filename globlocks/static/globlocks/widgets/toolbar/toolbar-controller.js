class ToolbarController extends window.StimulusModule.Controller {
    static values = { 
        target:             { type: String },
        tools:              { type: String },
        // object:              { default: {}, type: Object },
    };

    connect() {

        let tools = atob(this.toolsValue);
        try {
            tools = JSON.parse(tools);
        } catch (e) {
            throw new Error('ToolbarWidget requires a tools object');
        }
        this.toolbar = new ToolbarWidget(
            this.element.id,
            this.targetValue,
            tools,
        );
    }

    disconnect() {
        this.toolbar.disconnect();
        this.toolbar = null;
    }
}

window.wagtail.app.register('toolbar-widget', ToolbarController);
