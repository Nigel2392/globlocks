from wagtail import blocks
from django import forms
from globlocks.widgets.justify_widget import JustifyWidget

class JustifyBlock(blocks.ChoiceBlock):
    """
        A block that can be used to justify text.
    """
    justify_widget = JustifyWidget
    default_choices = JustifyWidget.default_choices

    def __init__(self, choices = None, targets: list[str] = None, **kwargs):
        
        if "widget" in kwargs:
            raise ValueError("widget is not allowed in JustifyBlock.")
        
        self.choices = choices or self.default_choices
        kwargs["default"] = self.choices[0][0]
        self.targets = targets or []
        super().__init__(**kwargs)

    def get_field(self, **kwargs):

        if "widget" in kwargs:
            del kwargs["widget"]

        return forms.ChoiceField(
            widget=self.justify_widget(
                choices=self.choices,
                targets=self.targets,
            ),
            **kwargs,
        )




