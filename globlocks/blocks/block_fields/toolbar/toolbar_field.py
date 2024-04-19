from django import forms
from typing import TYPE_CHECKING, Union, Any
if TYPE_CHECKING:
    from .bar import Tool

from globlocks.util import AutoJSONEncoder
from .toolbar_widget import (
    ToolbarWidget
)

from .tools import Tool
from .element import ElementType
from globlocks.settings import LOREM_IPSUM_SHORT
import json


class ToolbarValue:
    def __init__(self, tag_name: str, value: dict[str, Any], tools: list[Tool]):
        self.tag_name = tag_name
        self.value = value
        self.tools = tools

    def get_value(self):
        return self.value

    def create_element(self) -> ElementType:
        return ElementType(self, self.tag_name, self.value)
    
    def _json(self):
        return self.value
    
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


class ToolbarFormField(forms.JSONField):

    def __init__(self, targets: Union[str, list[str]] = None, tools: list["Tool"] = None, tag_name: str = "div", *args, **kwargs):
        self.tools = tools
        self.targets = targets
        self.tag_name = tag_name
        kwargs["encoder"] = AutoJSONEncoder
        super().__init__(*args, **kwargs)

    @property
    def widget(self):
        return ToolbarWidget(
            targets=self.targets,
            tools=self.tools,
            encoder=AutoJSONEncoder
        )
    
    @widget.setter
    def widget(self, value):
        pass

    def prepare_value(self, value: Any) -> Any:
        if value is None:
            return None
        
        if isinstance(value, str):
            return value
        
        if isinstance(value, ToolbarValue):
            value = value.get_value()
        
        return super().prepare_value(value)

    def to_python(self, value: Any) -> Any:
        value = super().to_python(value)
        return self.to_value(value)
    
    def to_value(self, value: dict[str, Any]) -> ToolbarValue:
        return ToolbarValue(self.tag_name, value, self.tools)
