import json
from django.forms import widgets
from wagtail.utils.widgets import WidgetWithScript
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter


class ColorInputWidget(WidgetWithScript, widgets.TextInput):
    template_name = "globlocks/widgets/color-input-widget.html"

    def __init__(self, attrs=None):
        attrs = attrs or {}
        super().__init__(attrs=attrs)

    def render_js_init(self, id_, name, value):
        return "new ColorInputWidget({0});".format(json.dumps(id_))

    class Media:
        css = {
            "all": [
                "globlocks/widgets/color_input/pickr.css",
            ]
        }
        js = [
            "globlocks/widgets/color_input/pickr.min.js",
            "globlocks/widgets/color_input/color-input-widget.js",
        ]


class ColorInputWidgetAdapter(WidgetAdapter):
    js_constructor = "globlocks.widgets.ColorInput"

    class Media:
        js = [
            "globlocks/widgets/color_input/pickr.min.js",
            "globlocks/widgets/color_input/color-input-widget-telepath.js",
        ]


register(ColorInputWidgetAdapter(), ColorInputWidget)
