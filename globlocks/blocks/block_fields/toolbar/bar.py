from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from wagtail import blocks

from typing import Any, Union
from .toolbar_field import ToolbarFormField
from .tools import Tool, DEFAULT_TOOLS, get_tool
from .element import ElementType


LOREM_IPSUM = getattr(settings,
    "GLOBLOCKS_LOREM_IPSUM",
    _("Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
)


class ToolbarValue:
    def __init__(self, tag_name: str, value: dict[str, Any], tools: list[Tool]):
        self.tag_name = tag_name
        self.value = value
        self.tools = tools


    def create_element(self) -> ElementType:
        return ElementType(self, self.tag_name, self.value)

    def render_text(self, text: str):
        """

        """
        element = self.create_element()
        return self.render_element(element, text)
    
    def render_element(self, element: ElementType, text: str):
        """
            Renders the element with the given value and text.
        """
        if self.value is not None:
            for tool in self.tools:
                if tool.tool_type in self.value and tool.should_format(self.value[tool.tool_type]):
                    element = tool.format(element, self.value[tool.tool_type])
        return element.render_text(text)

    def __str__(self):
        """
            Renders the value with a default lorem ipsum text.
        """
        return self.render_text(LOREM_IPSUM)
    

class ToolbarBlock(blocks.FieldBlock):
    MUTABLE_META_ATTRIBUTES = [
        "value_class",
        "tag_name",
    ]

    class Meta:
        value_class = ToolbarValue
        tag_name = "div"

    def __init__(
        self,
        target: str = None,
        tools: list[Union[Tool, str]] = None,
        required=False,
        help_text=None,
        validators=(),
        **kwargs,
    ):
        
        if tools is None:
            tools = DEFAULT_TOOLS

        self.tools = tools
        self.target = target
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "validators": validators,
        }

        super().__init__(**kwargs)

    def value_for_form(self, value: ToolbarValue):
        """
        Reverse of value_from_form; convert a value of this block's native value type
        to one that can be rendered by the form field
        """
        if isinstance(value, ToolbarValue):
            return super().value_for_form(value.value)
        
        return super().value_for_form(value)


    def value_from_form(self, value) -> ToolbarValue:
        """
        The value that we get back from the form field might not be the type
        that this block works with natively; for example, the block may want to
        wrap a simple value such as a string in an object that provides a fancy
        HTML rendering (e.g. EmbedBlock).

        We therefore provide this method to perform any necessary conversion
        from the form field value to the block's native value. As standard,
        this returns the form field value unchanged.
        """
        value = super().value_from_form(value)
        return ToolbarValue(self.meta.tag_name, value, self.tools_list)
    

    def to_python(self, value):
        """
        Convert 'value' from a simple (JSON-serialisable) value to a (possibly complex) Python value to be
        used in the rest of the block API and within front-end templates . In simple cases this might be
        the value itself; alternatively, it might be a 'smart' version of the value which behaves mostly
        like the original value but provides a native HTML rendering when inserted into a template; or it
        might be something totally different (e.g. an image chooser will use the image ID as the clean
        value, and turn this back into an actual image object here).
        """
        if isinstance(value, ToolbarValue):
            return value
        return ToolbarValue(self.meta.tag_name, value, self.tools_list)


    def get_prep_value(self, value):
        """
        The reverse of to_python; convert the python value into JSON-serialisable form.
        """
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
            target=self.target,
            tools=self.tools_list,
            **self.field_options,
        )

