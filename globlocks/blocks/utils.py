from wagtail import blocks


class AttrMixin:
    def __init__(self, *args, attrs = None, **kwargs):
        super().__init__(*args, **kwargs)
        if attrs:
            self.field.widget.attrs.update(attrs)


class CharBlockWithAttrs(AttrMixin, blocks.CharBlock):
    pass

class URLBlockWithAttrs(AttrMixin, blocks.URLBlock):
    pass

class EmailBlockWithAttrs(AttrMixin, blocks.EmailBlock):
    pass
