from django.template import library
from ..preview import PreviewUnavailable, preview_of_block


register = library.Library()


@register.simple_tag(name="render_as_preview", takes_context=True)
def render_as_preview(context, block, fail_silently=False, **kwargs):
    try:
        v = preview_of_block(block, context, fail_silently=fail_silently, **kwargs)
        if v is None:
            return ""
        return v
    except PreviewUnavailable:
        return block

