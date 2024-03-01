from wagtail import blocks
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from ...fields.orderablefield import Orderable, OrderableFormField
from ...widgets.orderable import OrderableWidget


class OrderableBlock(blocks.FieldBlock):
    def __init__(
        self,
        orderables: list[Orderable] = None,
        required=True,
        help_text=None,
        validators=(),
        **kwargs,
    ):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
            "orderables": orderables,
            "widget": OrderableWidget(
                orderables=orderables,
            ),
        }

        super().__init__(**kwargs)

    @cached_property
    def field(self):
        return OrderableFormField(**self.field_options)

