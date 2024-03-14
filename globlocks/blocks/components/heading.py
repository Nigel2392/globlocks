from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from ..block_fields import (
    toolbar,
)
from ..bases import (
    ToggleShowableConfiguration,
    ToggleShowableBlock,
)


class HeadingConfiguration(ToggleShowableConfiguration):
    toolbar = toolbar.ToolbarBlock(
        targets=[
            "heading",
            "subheading"
        ],
        tag_name="h2",
        tools = [
            "BOLD",
            "ITALIC",
            "UNDERLINE",
            "STRIKETHROUGH",
            "JUSTIFY_LEFT",
            "JUSTIFY_CENTER",
            "JUSTIFY_RIGHT",
            "HEADING_2",
            "HEADING_3",
            "HEADING_4",

        ],
        required=False,
        label=_("Toolbar"),
        help_text=_("Format your heading and subheading."),
    )

    class Meta:
        label = _("Configuration")
        icon = "cog"
        button_label = _("Open Settings")
        label_format = _("Heading Configuration")
        absolute_position = True

class Heading(ToggleShowableBlock):
    advanced_settings_class = HeadingConfiguration

    heading = blocks.CharBlock(
        required=True,
        help_text=_("The heading of the block."),
        form_classname="title",
    )

    subheading = blocks.CharBlock(
        required=False,
        help_text=_("The subheading of the block."),
    )

    class Meta:
        group=_("Text")
        icon = "title"
        label = _("Heading")
        label_format = _("Heading: {heading}")
        template = "globlocks/blocks/components/heading/heading.html"

