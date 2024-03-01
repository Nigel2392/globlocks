from typing import Union
from wagtail.blocks import StreamValue, StructValue
from wagtail.blocks.list_block import ListValue
from django.utils.safestring import mark_safe, SafeString

from globlocks.blocks.bases import BaseBlock


class PreviewUnavailable(Exception):
    pass


def preview_of_block(block, context, fail_silently: bool = False, **kwargs) -> Union[str, SafeString]:
    if isinstance(block, (StreamValue, ListValue)):
        p = []
        for child in block:
            child: Union[StreamValue.StreamChild, ListValue.ListChild]
            rendered = preview_of_block(child, context, fail_silently=fail_silently, **kwargs)
            if rendered: p.append(rendered)
        return mark_safe("".join(p))
            
    elif isinstance(block, (StreamValue.StreamChild, ListValue.ListChild))\
         and isinstance(block.block, BaseBlock):
        
        rendered = block.block.render_as_preview(block.value, context, **kwargs)
        return rendered or ""
    
    elif isinstance(block, StructValue) and isinstance(block.block, BaseBlock):
        rendered = block.block.render_as_preview(block, context, **kwargs)
        return rendered or ""

    elif hasattr(block, "block") and hasattr(block.block, "render_as_preview"):
        rendered = block.block.render_as_preview(block.value, context, **kwargs)
        return rendered or ""
    
    elif hasattr(block, "render_as_preview"): # Special case
        rendered = block.render_as_preview(context, **kwargs)
        return rendered or ""

    if not fail_silently:
        raise PreviewUnavailable(f"Preview not available for {block}")
    
    return ""
