from django.forms import widgets
from wagtail.utils.widgets import WidgetWithScript
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter
import json


class RangeInput(WidgetWithScript, widgets.Input):
    template_name = "globlocks/widgets/slider_input.html"
    input_type = "range"
    unit = ""

    def __init__(self, unit="", stepping=1, max=None, min=None, *args, **kwargs):
        self.unit = unit
        self.stepping = stepping
        self.max = max
        self.min = min
        super().__init__(*args, **kwargs)

    def render_js_init(self, id_, name, value):
        return f"""new RangeSlider(
            {json.dumps(id_)},
            {json.dumps(value)},
            {json.dumps(self.unit)},
        )"""

    def get_context(self, name: str, value, attrs):
        ctx = super().get_context(name, value, attrs)
        ctx["widget"]["value"] = value
        ctx["widget"]["unit"] = self.unit
        ctx["widget"]["stepping"] = self.stepping
        ctx["widget"]["max"] = self.max
        ctx["widget"]["min"] = self.min
        return ctx

    class Media:
        js = ("globlocks/widgets/range_slider/range-slider.js",)
        css = {"all": ("globlocks/widgets/range_slider/range-slider.css",)}


class RangeInputWidgetAdapter(WidgetAdapter):
    js_constructor = "globlocks.widgets.RangeInput"

    def js_args(self, widget):
        s = super().js_args(widget)
        s.append(widget.unit)
        return s

    class Media:
        js = [
            "globlocks/widgets/range_slider/range-slider-telepath.js",
        ]


register(RangeInputWidgetAdapter(), RangeInput)
