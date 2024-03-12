from django import forms
from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .bar import Tool

from globlocks.util import AutoJSONEncoder
from .toolbar_widget import (
    ToolbarWidget
)


class ToolbarFormField(forms.JSONField):

    def __init__(self, targets: Union[str, list[str]] = None, tools: list["Tool"] = None, *args, **kwargs):
        self.tools = tools
        self.targets = targets
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

