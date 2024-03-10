class JustifyController extends window.StimulusModule.Controller {
    static values = { 
        targets: {default: [], type: Array},
    };

    connect() {

        console.log('JustifyController connected', this, this.targetsValue);

        this.justifier = new JustifyWidget(
            this.element.id,
            this.element.value,
            this.targetsValue,
        );
    }

    disconnect() {
        this.justifier.disconnect();
        this.justifier = null;
    }
}

window.wagtail.app.register('justify-widget', JustifyController);
