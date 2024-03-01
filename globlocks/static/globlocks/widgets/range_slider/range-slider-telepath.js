

(function() {
    function RangeSliderInput(html, _, unit) {
        this.html = html;
        this.unit = unit;
    }
    RangeSliderInput.prototype.render = function(placeholder, name, id, initialState) {
        var html = this.html.replace(/__NAME__/g, name).replace(/__ID__/g, id);
        placeholder.outerHTML = html;


        var rangeSlider = new RangeSlider(id, null, this.unit);
        rangeSlider.setState(initialState);
        return rangeSlider;
    };

    window.telepath.register('globlocks.widgets.RangeInput', RangeSliderInput);
})();
