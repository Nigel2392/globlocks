from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks

from typing import Any, Union
from .toolbar_field import ToolbarFormField
from .tools import Tool, DEFAULT_TOOLS, get_tool
from .element import ElementType
from globlocks.settings import LOREM_IPSUM_SHORT


class ToolbarValue:
    def __init__(self, tag_name: str, value: dict[str, Any], tools: list[Tool]):
        self.tag_name = tag_name
        self.value = value
        self.tools = tools

    def get_value(self):
        return self.value

    def create_element(self) -> ElementType:
        return ElementType(self, self.tag_name, self.value)
    
    def _generate_element(self, element: ElementType = None, **kwargs) -> ElementType:
        if element is None:
            element = self.create_element()

        for tool in self.tools:
            if tool.tool_type in self.value and tool.should_format(self.value[tool.tool_type]):
                element = tool.format(element, self.value[tool.tool_type])

        for key, value in kwargs.items():
            if value is not None:
                element.attrs.add(key, value)

        return element
    
    def render_text(self, text: str, **kwargs):
        """

        """
        element = self.create_element()
        return self.render_element(element, text, **kwargs)
    
    def render_element(self, element: ElementType, text: str, **kwargs):
        """
            Renders the element with the given value and text.
        """
        element = self._generate_element(element, **kwargs)
        return element.render_text(text)

    def __str__(self):
        """
            Renders the value with a default lorem ipsum text.
        """
        return self.render_text(LOREM_IPSUM_SHORT)
    

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
        {% load globlocks_.toolbar %}
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
        if isinstance(value, ToolbarValue):
            return super().value_for_form(value.value)
        
        return super().value_for_form(value)

    def value_from_form(self, value) -> ToolbarValue:
        value = super().value_from_form(value)
        return ToolbarValue(self.meta.tag_name, value, self.tools_list)

    def to_python(self, value):
        if isinstance(value, ToolbarValue):
            return value
        return ToolbarValue(self.meta.tag_name, value, self.tools_list)

    def get_prep_value(self, value):
        if isinstance(value, ToolbarValue):
            return super().get_prep_value(value.value)
        return super().get_prep_value(value)

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
            **self.field_options,
        )

