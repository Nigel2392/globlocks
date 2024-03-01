
(function() {
    function FontPickerWidgetFunc(html) {
        this.html = html;
    }
    FontPickerWidgetFunc.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        initialState = JSON.parse(initialState);

        var orderableInput = new FontPickerWidget(id, initialState);
        
        return orderableInput;
    };

    window.telepath.register('globlocks.widgets.FontPickerWidget', FontPickerWidgetFunc);
})();
