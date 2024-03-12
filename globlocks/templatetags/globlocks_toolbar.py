from typing import Tuple
from django.template import library
from django.template import (
    TemplateSyntaxError,
)

from ..blocks import toolbar


register = library.Library()

def _valid_toolbar_value(value):
    if not value or not isinstance(value, toolbar.ToolbarValue):
        raise TemplateSyntaxError("apply_toolbar tag requires a toolbar value")


@register.filter(name="t_style")
def t_style(styleAttr: str, styleValue: str) -> str:
    """
        Helper tag for adding styles inside of your templates to the toolbar.

        (returns a tuple of styleAttr, styleValue)

        Example:
        ```django-template
        {% apply_toolbar ... style="color"|t_style:"red" %}
        ```
    """
    if not styleAttr or not styleValue:
        return None

    return (styleAttr, styleValue)
    

@register.simple_tag(name="apply_toolbar")
def apply_toolbar(target_value: str, toolbar_value: toolbar.ToolbarValue, **kwargs):
    """
        Apply the toolbar to the target value.

        Example:

        ```django-template
        {% apply_toolbar self.text self.settings.toolbar class="my extra class" %}
        ```
    """
    if not target_value:
        return ""
    
    _valid_toolbar_value(toolbar_value)
    
    element: toolbar.ElementType = toolbar_value.create_element()
    for k, *v in kwargs.items():
        if all([val is not None for val in v]):
            element.attrs.add(k, *v)
    return toolbar_value.render_element(element, target_value)


@register.simple_tag(name="toolbar_attributes")
def toolbar_attributes(toolbar_value: toolbar.ToolbarValue, **kwargs) -> Tuple[str, toolbar.Attributes]:
    """
        Get attributes from the toolbar to generate your own target value.

        Example:

        ```django-template
        {% toolbar_attributes ... as tagname, attributes %}

        <{{ tagname }} {{ attributes|safe }}>
            ...
        </{{ tagname }}>
        ```
    """

    _valid_toolbar_value(toolbar_value)

    element: toolbar.ElementType = toolbar_value.create_element()
    for k, *v in kwargs.items():
        if all([val is not None for val in v]):
            element.attrs.add(k, *v)

    return element.generate()

