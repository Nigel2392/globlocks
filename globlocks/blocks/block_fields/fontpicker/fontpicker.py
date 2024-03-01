from wagtail import blocks
from django import forms
from django.utils.functional import cached_property
from ....widgets.fontpicker import FontPickerWidget


class FontPickerBlock(blocks.FieldBlock):
    def __init__(
        self,
        min,
        max,
        fonts: list = None,
        stepping=1,
        unit="em",
        required=True,
        help_text=None,
        preview_text=None,
        **kwargs
    ):
        self.field_options = {
            "required": required,
            "help_text": help_text,
        }
        self.unit = unit
        self.min = min
        self.max = max
        self.stepping = stepping
        self.fonts = fonts
        self.preview_text = preview_text
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {
            "widget": FontPickerWidget(
                preview_text=self.preview_text,
                unit=self.unit,
                min=self.min,
                max=self.max,
                stepping=self.stepping,
                fonts=self.fonts,
            ),
        }
        field_kwargs.update(self.field_options)
        return forms.JSONField(**field_kwargs)
