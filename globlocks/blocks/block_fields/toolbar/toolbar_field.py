from django import forms
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .bar import Tool

from globlocks.util import AutoJSONEncoder
from .toolbar_widget import (
    ToolbarWidget
)


class ToolbarFormField(forms.JSONField):

    def __init__(self, target: str = None, tools: list["Tool"] = None, *args, **kwargs):
        self.tools = tools
        self.target = target
        kwargs["encoder"] = AutoJSONEncoder
        super().__init__(*args, **kwargs)

    @property
    def widget(self):
        return ToolbarWidget(
            target=self.target,
            tools=self.tools,
            encoder=AutoJSONEncoder
        )
    
    @widget.setter
    def widget(self, value):
        pass

