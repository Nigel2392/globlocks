from django import forms
from wagtail import blocks
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from ...fields.orderablefield import (
    _OrderablePythonValueMixin,
    Orderable, OrderableFormField,
    _if_call,
)
from ...widgets.orderable import OrderableWidget



class OrderableBlock(_OrderablePythonValueMixin, blocks.FieldBlock):
    def __init__(
        self,
        orderables: list[Orderable] = None,
        required=True,
        help_text=None,
        validators=(),
        **kwargs,
    ):
        self.orderables = orderables
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
    
    def get_prep_value(self, value):
        if value is None:
            return super().get_prep_value(value)
        
        for i in range(len(value)):
            if isinstance(value[i], Orderable):
                value[i] = value[i].value

        return super().get_prep_value(value)

    def get_default(self):
        default = super().get_default()
        if default:
            return default
        
        orderables = _if_call(self.orderables)
        return orderables

    def clean(self, value):
        value = super().clean(value)
        if not value:
            return value

        orderables = _if_call(self.orderables)
        values = [orderable.value for orderable in orderables]
        for v in value:
            if isinstance(v, Orderable):
                v = v.value
            if v not in values:
                raise forms.ValidationError(_("Invalid value: %(value)s"), params={"value": v})

        return value
