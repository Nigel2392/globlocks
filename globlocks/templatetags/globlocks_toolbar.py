from django.template import library
from django.template import (
    TemplateSyntaxError,
)

from ..blocks import toolbar


register = library.Library()



@register.simple_tag(name="apply_toolbar")
def apply_toolbar(target_value: str, toolbar_value: toolbar.ToolbarValue, **kwargs):
    """
        Apply the toolbar to the target value.
    """
    if not target_value:
        return ""
    
    if not toolbar_value or\
        not isinstance(toolbar_value, toolbar.ToolbarValue):

        raise TemplateSyntaxError("apply_toolbar tag requires a toolbar value")
    
    element: toolbar.ElementType = toolbar_value.create_element()
    for k, v in kwargs.items():
        if v is not None and v != "":
            element.attrs.add(k, v)
    return toolbar_value.render_element(element, target_value)




