from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from conditional_field import (
    parent as parent_queryselector,
    classname as make_classname,
    SHOW,
)

from ... import (
    block_fields,
    bases,
)
from ...block_fields import (
    JustifyBlock,
)
from ...bases import (
    TemplateBlockConfiguration,
    TemplateBlock,
    ToggleableConfig,
    ToggleableBlock,
)
from ..link import (
    Link,
)



class FlatMenuItem(blocks.StructBlock):
    """
        A block for a menu item.
    """

    ALLOWED_FEATURES = [
        "page", "document", "external",
    ]

    image = ImageChooserBlock(
        required=False,
        help_text=_("An image to display with the menu item."),
        classname=make_classname(
            SHOW(1, "custom_template"),
            parent_queryselector("class", "globlocks-showable-block")
        )
    )

    link = Link(
        help_text=_("Where do you want to link to?"),
        features=ALLOWED_FEATURES,
        no_row_padding = False,
        stacked = False,
    )

    class Meta:
        icon = "list-ul"
        label = _("Menu Item")
        label_format = _("Menu Item: {label}")


class FlatMenuConfiguration(ToggleableConfig, TemplateBlockConfiguration):
    alignment = JustifyBlock(
        targets=[
            "title",
            "subtitle",
            "text",
        ]
    )

    class Meta:
        icon = "list-ul"

class FlatMenu(ToggleableBlock, TemplateBlock):
    advanced_settings_class = FlatMenuConfiguration

    templates = (
        ("globlocks/blocks/components/menus/flat/vertical.html", _("Vertical")),
        ("globlocks/blocks/components/menus/flat/horizontal.html", _("Horizontal")),
    )

    title = blocks.CharBlock(
        required=False,
        help_text=_("The title of the menu."),
    )

    subtitle = blocks.RichTextBlock(
        required=False,
        help_text=_("The subtitle of the menu."),
        features=["bold", "italic", "link"],
    )

    items = blocks.ListBlock(
        FlatMenuItem(),
        required=False,
        help_text=_("The items in the menu."),
    )

    class Meta:
        icon = "list-ul"
        group=_("Menus")
        label = _("Flat Menu")
        label_format = _("Flat Menu: {title}")
        template = "globlocks/blocks/components/menus/flat.html"

