from wagtail import blocks
from django import forms
from django.utils.functional import cached_property
from ....widgets.color_input_widget import ColorInputWidget


class ColorBlock(blocks.FieldBlock):
    def __init__(self, required=True, help_text=None, validators=(), **kwargs):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "max_length": 255,
            "min_length": 3,
        }
        super().__init__(**kwargs)

    @cached_property
    def field(self):
        field_kwargs = {"widget": ColorInputWidget()}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    class Meta:
        icon = "radio-full"
        translatable=False
