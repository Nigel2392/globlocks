from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter
from wagtail.utils.widgets import WidgetWithScript
import json

from ..util import AutoJSONEncoder
from ..fonts import FONT_LIST, Font

class FontPickerWidget(WidgetWithScript):
    template_name = "globlocks/widgets/font_picker_widget.html"

    def __init__(
        self,
        attrs=None,
        fonts: list[Font] = None,
        preview_text: str = None,
        encoder=AutoJSONEncoder,
        unit="em",
        min=0.1,
        max=100,
        stepping=0.1,
        *args,
        **kwargs,
    ):
        if not fonts:
            fonts = FONT_LIST

        if not isinstance(fonts, list) and not isinstance(fonts, tuple):
            raise ValueError("Fonts must be a list or tuple")

        self.unit = unit
        self.fonts = fonts
        self.preview_text = preview_text
        self.default_font = fonts[0] if len(fonts) > 0 else None
        self.encoder = encoder
        self.min = min
        self.max = max
        self.stepping = stepping
        super().__init__(attrs=attrs, *args, **kwargs)

    def value_from_datadict(self, data, files, name):
        font = data.get(name, self.default_font)
        size = data.get(f"{name}-size", None)
        font = json.loads(font)
        if isinstance(font, str):
            return json.dumps(self.default)
        return json.dumps({
            "name": font.get("name", self.default_font.name),
            "path": font.get("path", self.default_font.path),
            "size": size,
            "unit": self.unit or "em",
        })

    @property
    def default(self):
        return {
            "name": self.default_font.name,
            "path": self.default_font.path,
            "size": 1,
            "unit": self.unit or "em",
        }

    def get_value_data(self, value=None):
        if value and (isinstance(value, str) and value.lower() != "null"):
            v = json.loads(value)
        elif value:
            v = value
        else:
            v = self.default
        return v

    def render_js_init(self, id_, name, value):
        return f"new FontPickerWidget(`{id_}`, {json.dumps(value or self.default, cls=self.encoder)}, {json.dumps(self.unit)});"

    def get_context(self, name: str, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["fonts"] = self.fonts
        context["widget"]["preview_text"] = self.preview_text
        context["widget"]["abs_value"] = value
        context["widget"]["unit"] = self.unit
        context["widget"]["min"] = self.min
        context["widget"]["max"] = self.max
        context["widget"]["stepping"] = self.stepping
        return context

    class Media:
        css = {
            "all": [
                "globlocks/widgets/font_picker/font-picker.css",
            ]
        }
        js = [
            "globlocks/widgets/font_picker/font-picker-widget.js",
        ]


class FontPickerWidgetAdapter(WidgetAdapter):
    js_constructor = "globlocks.widgets.FontPickerWidget"

    class Media:
        js = [
            "globlocks/widgets/font_picker/font-picker-telepath.js",
        ]


register(FontPickerWidgetAdapter(), FontPickerWidget)
