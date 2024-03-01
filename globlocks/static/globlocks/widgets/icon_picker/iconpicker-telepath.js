
(function() {
    function IconPickerWidgetFunc(html) {
        this.html = html;
    }
    IconPickerWidgetFunc.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        return new IconPickerWidget(`#${id}`, initialState);
    };

    window.telepath.register('globlocks.widgets.IconPickerWidget', IconPickerWidgetFunc);
})();
