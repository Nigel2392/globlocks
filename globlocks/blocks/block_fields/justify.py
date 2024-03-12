from wagtail import blocks
from globlocks.widgets.justify_widget import JustifyWidget

class JustifyBlock(blocks.ChoiceBlock):
    """
        A block that can be used to justify text.
    """
    justify_widget = JustifyWidget
    default_choices = JustifyWidget.default_choices

    def __init__(self, choices = None, targets: list[str] = None, **kwargs):
        kwargs["widget"] = self.justify_widget(
            choices=choices or self.default_choices,
            targets=targets,
        )
        super().__init__(**kwargs)


