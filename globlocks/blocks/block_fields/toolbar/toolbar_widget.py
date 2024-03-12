import base64
from functools import cached_property
from typing import Union
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
import json

from globlocks.util import AutoJSONEncoder
from .tools import Tool, get_tool



class ToolbarWidget(widgets.Input):
    tools: list["Tool"] = None
    template_name = "globlocks/widgets/toolbar-widget.html"

    def __init__(
        self, attrs=None, targets: Union[str, list[str]] = None, tools: Union[list[Union["Tool", str]], callable] = None, encoder=AutoJSONEncoder
    ):
        default_attrs = {
            "class": "toolbar-widget",
        }
        attrs = attrs or {}
        attrs = {**default_attrs, **attrs}

        if not targets:
            raise ValueError("target must be specified")

        if not tools and not self.tools:
            raise ValueError("tools must be specified")
        
        if not isinstance(targets, (list, tuple)):
            targets = [targets]
        
        self.tools = tools or self.tools
        self.targets = targets
        self.encoder = encoder

        super().__init__(attrs=attrs)

    @cached_property
    def tools_list(self) -> list["Tool"]:
        if callable(self.tools):
            tools = self.tools()
        else:
            tools = self.tools

        return [get_tool(tool) for tool in tools]

    def build_attrs(self, base_attrs, extra_attrs):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-controller"] = "toolbar-widget"
        attrs["data-toolbar-widget-targets-value"] = base64.b64encode(
            json.dumps(
            self.targets,
            cls=self.encoder
        ).encode("utf-8")).decode("utf-8")
        attrs["data-toolbar-widget-tools-value"] = base64.b64encode(
            json.dumps(
            self.tools_list,
            cls=self.encoder
        ).encode("utf-8")).decode("utf-8")
        return attrs
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["tools"] = self.tools_list
        return context

    @property
    def media(self):
        media = widgets.Media(
            css = {"all": ["globlocks/widgets/toolbar/toolbar-widget.css"]},
            js = [
                "globlocks/widgets/utils.js",
                "globlocks/widgets/toolbar/toolbar-widget.js",
                "globlocks/widgets/toolbar/toolbar-controller.js",
            ]
        )
        for tool in self.tools_list:
            media += tool.media

        return media

