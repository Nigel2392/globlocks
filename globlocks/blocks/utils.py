from wagtail import blocks
from django import forms


class AttrMixin:
    def __init__(self, *args, attrs = None, **kwargs):
        super().__init__(*args, **kwargs)
        if attrs:
            self.field.widget.attrs.update(attrs)


class CharBlockWithAttrs(AttrMixin, blocks.CharBlock):

    def clean(self, value):
        value = super().clean(value)
        value = value.strip()
        if len(value) > self.field.max_length:
            raise forms.ValidationError({self.name: f"Ensure this value has at most {self.field.max_length} characters (it has {len(value)})"})
        return value

class URLBlockWithAttrs(AttrMixin, blocks.URLBlock):
    pass

class EmailBlockWithAttrs(AttrMixin, blocks.EmailBlock):
    pass
