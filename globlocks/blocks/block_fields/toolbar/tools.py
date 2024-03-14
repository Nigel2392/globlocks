from typing import TYPE_CHECKING, Any, Union
from django.forms import widgets
import re

from globlocks.settings import GLOBLOCKS_TOOLSTYLES_ADD_CLASSES
from globlocks import util

if TYPE_CHECKING:
    from .element import (
        ElementType,
    )

class Tool:
    label: str
    icon_name: str
    tool_type: str
    js: list[str]
    css: list[str]

    def __init__(self, label, icon_name, tool_type, js=None, css=None):
        self.label = label
        self.icon_name = icon_name
        self.tool_type = tool_type
        self.js = js or []
        self.css = css or []

    def json(self):
        return str(self.tool_type)

    @property
    def media(self):
        return widgets.Media(js=self.js, css={"all": self.css})

    def should_format(self, value: Any) -> bool:
        return not not value
    
    def format(self, element: "ElementType", value: Any) -> "ElementType":
        pass



class StyleTool(Tool):
    def __init__(self, icon_name, tool_type, style_name, style_value):
        super().__init__(None, icon_name, tool_type)
        self.style_name = style_name
        self.style_value = style_value

    def should_format(self, value: Any) -> bool:
        if isinstance(value, (list, tuple)):
            return self.style_value in value
        elif isinstance(value, str):
            return re.search(rf"\b{self.style_value}\b", value)
        return False

    def format(self, element: "ElementType", value: Any) -> "ElementType":
        if GLOBLOCKS_TOOLSTYLES_ADD_CLASSES:
            element.attrs.add("class", f"{self.style_name}-{self.style_value}")
            return element
        
        if value:
            element.attrs.add("style", self.style_name, self.style_value)
        else:
            element.attrs.remove("style", self.style_name, self.style_value)
        return element

class HeadingTool(Tool):
    def __init__(self, tag_name, tool_type, js=None, css=None):
        super().__init__(None, f"text-{tag_name}", tool_type, js, css)
        self.tag_name = tag_name

    def should_format(self, value: Any) -> bool:
        return (not not value) and (value == self.tag_name)

    def format(self, element: "ElementType", value: Any) -> "ElementType":
        element.tag = self.tag_name
        return element


class ColorTool(Tool):
    def __init__(self, icon_name, tool_type, colorAttr, js=None, css=None):
        super().__init__(None, icon_name, tool_type, js, css)
        self.colorAttr = colorAttr

    def should_format(self, value: Any) -> bool:
        return True

    def format(self, element: "ElementType", value: Any) -> "ElementType":
        element.attrs.add("style", self.colorAttr, value)
        return element


ToolBold = StyleTool("text-bold", "BOLD", "font-weight", "bold")
ToolItalic = StyleTool("text-italic", "ITALIC", "font-style", "italic")
ToolUnderline = StyleTool("text-underline", "UNDERLINE", "text-decoration", "underline")
ToolStrikethrough = StyleTool("text-strikethrough", "STRIKETHROUGH", "text-decoration", "line-through")
ToolJustifyLeft = StyleTool("text-left", "JUSTIFY_LEFT", "text-align", "left")
ToolJustifyCenter = StyleTool("text-center", "JUSTIFY_CENTER", "text-align", "center")
ToolJustifyRight = StyleTool("text-right", "JUSTIFY_RIGHT", "text-align", "right")

ToolHeading1 = HeadingTool("h1", "HEADING_1")
ToolHeading2 = HeadingTool("h2", "HEADING_2")
ToolHeading3 = HeadingTool("h3", "HEADING_3")
ToolHeading4 = HeadingTool("h4", "HEADING_4")
ToolHeading5 = HeadingTool("h5", "HEADING_5")
ToolHeading6 = HeadingTool("h6", "HEADING_6")
TextColorTool = ColorTool("text-palette", "COLOR",
    colorAttr="color",
    js=["globlocks/widgets/color_input/pickr.min.js"],
    css=["globlocks/widgets/color_input/pickr.css"]
)
BackgroundColorTool = ColorTool("text-palette-fill", "BACKGROUND_COLOR",
    colorAttr="background-color",
    js=["globlocks/widgets/color_input/pickr.min.js"],
    css=["globlocks/widgets/color_input/pickr.css"]
)


DEFAULT_TOOLS = [
    ToolBold,
    ToolItalic,
    ToolUnderline,
    ToolStrikethrough,
    ToolJustifyLeft,
    ToolJustifyCenter,
    ToolJustifyRight,
    ToolHeading1,
    ToolHeading2,
    ToolHeading3,
    ToolHeading4,
    ToolHeading5,
    ToolHeading6,
    TextColorTool,
    BackgroundColorTool,
]

tools = {
    tool.tool_type: tool
    for tool in DEFAULT_TOOLS
}

_registered_all_tools = False

def _register_all_tools():
    global _registered_all_tools
    if _registered_all_tools:
        raise Exception("Already registered all tools")

    h = util.get_hooks("register_toolbar_tools")
    for hook in h:
        hook(tools)

def get_tool(tool_name: Union[str, Tool]) -> Tool:
    global _registered_all_tools
    if not _registered_all_tools:
        _register_all_tools()

    if isinstance(tool_name, str):
        if tool_name not in tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return tools[tool_name]
    
    return tool_name
