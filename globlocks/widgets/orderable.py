from typing import Union
from django.forms import widgets
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter
from wagtail.utils.widgets import WidgetWithScript
import json

from ..util import AutoJSONEncoder

class OrderableWidget(WidgetWithScript, widgets.Input):
    orderables: list = None
    template_name = "globlocks/widgets/orderable_widget.html"

    def __init__(
        self, attrs=None, orderables: Union[list, callable] = None, encoder=AutoJSONEncoder
    ):
        default_attrs = {
            "class": "orderable-widget",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}
        if not orderables:
            raise ValueError("Orderables must be specified")
        self.orderables = orderables
        self.encoder = encoder
        super().__init__(attrs=attrs)

    def render_js_init(self, id_, name, value):
        return (
            f"new OrderableWidget(`{id_}`, {json.dumps(value or [], cls=self.encoder)});"
        )

    def get_context(self, name: str, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["items"] = (
            self.orderables() if callable(self.orderables) else self.orderables
        )
        return context

    class Media:
        css = {
            "all": [
                "globlocks/widgets/orderable/orderable.css",
            ]
        }
        js = [
            "globlocks/widgets/orderable/orderable.js",
            "globlocks/widgets/orderable/sortable.min.js",
        ]


class OrderableWidgetAdapter(WidgetAdapter):
    js_constructor = "globlocks.widgets.OrderableWidget"

    class Media:
        js = [
            "globlocks/widgets/orderable/orderable-telepath.js",
        ]
        


register(OrderableWidgetAdapter(), OrderableWidget)
