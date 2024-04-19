from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from typing import Any, Union
from .tools import Tool, get_tool, DEFAULT_TOOLS
from .toolbar_field import (
    ToolbarFormField,
    ToolbarValue,
)
import json
    

class ToolbarBlock(blocks.FieldBlock):
    """
        A block which provides a toolbar for a given element.
        This can be used to provide a nice interface for styling a single element,
        such as a CharBlock or TextBlock.

        Note:
            The toolbar cannot be used with non-text inputs.


        Example:
        ```python
        # blocks.py
        class MyBlock(blocks.StructBlock):
            toolbar = toolbar.ToolbarBlock(
                tag_name="p",
                target="text",
                required=False,
                label=_("Toolbar"),
                tools=[
                    # ... tools
                ]
            )
            text = blocks.CharBlock(
                required=True,
                label=_("Text"),
            )

            class Meta:
                template = "myapp/heading.html"
        ```

        And in the template:
        ```django-template
        {# myapp/heading.html #}
        {% load globlocks.toolbar %}
        {% apply_toolbar self.text self.settings.toolbar class="my extra class" %}
        ```
    """

    MUTABLE_META_ATTRIBUTES = blocks.FieldBlock.MUTABLE_META_ATTRIBUTES + [
        "value_class",
        "tag_name",
    ]

    class Meta:
        value_class = ToolbarValue
        tag_name = "div"

    def __init__(
        self,
        targets: Union[str, list[str]] = None,
        tools: list[Union[Tool, str]] = None,
        required=False,
        help_text=None,
        validators=(),
        **kwargs,
    ):
        
        if tools is None:
            tools = DEFAULT_TOOLS

        self.tools = tools
        self.targets = targets
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
        }

        super().__init__(**kwargs)

    def value_for_form(self, value: ToolbarValue):
        if value is None:
            return None
        
        if isinstance(value, str):
            return value
        
        return self.get_prep_value(value)

    def value_from_form(self, value) -> ToolbarValue:
        if isinstance(value, ToolbarValue):
            return value

        return self.to_python(value)

    def to_python(self, value):
        return self.field.to_python(value)

    def get_prep_value(self, value):
        return self.field.prepare_value(value)

    @cached_property
    def tools_list(self):
        if callable(self.tools):
            tools = self.tools()
        else:
            tools = self.tools
        return [get_tool(tool) for tool in tools]

    @cached_property
    def field(self):
        return ToolbarFormField(
            targets=self.targets,
            tools=self.tools_list,
            tag_name=self.meta.tag_name,
            **self.field_options,
        )

