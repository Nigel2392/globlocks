from wagtail import blocks
from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from ....widgets.range_input import RangeInput


class RangeSliderBlock(blocks.FieldBlock):
    def __init__(
        self,
        unit: str = "",
        required=True,
        help_text=None,
        max_value=None,
        min_value=None,
        stepping=1,
        validators=(),
        **kwargs,
    ):
        self.field_options = {
            "required": required,
            "stepping": stepping,
            "max": max_value,
            "min": min_value,
            "help_text": help_text,
            "validators": validators,
            "unit": unit,
        }

        try:
            default = int(kwargs.get("default", 0))
        except ValueError:
            default = 0
        kwargs["default"] = default

        super().__init__(**kwargs)

    @cached_property
    def field(self):
        return RangeField(**self.field_options)


class RangeField(forms.FloatField):
    widget = RangeInput

    def __init__(self, min=None, max=None, stepping=None, unit="", *args, **kwargs):
        self.min = min
        self.max = max
        self.stepping = stepping
        self.unit = unit
        self.widget = RangeInput(
            unit=unit,
            min=min,
            max=max,
            stepping=stepping,
        )
        super().__init__(*args, **kwargs)
