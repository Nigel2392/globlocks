
(function() {
    function OrderableInputWidget(html) {
        this.html = html;
    }
    OrderableInputWidget.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;

        var orderableInput = new OrderableInput(id, initialState);
        return orderableInput;
    };

    window.telepath.register('globlocks.widgets.OrderableWidget', OrderableInputWidget);
})();
