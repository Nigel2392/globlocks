from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from conditional_field import (
    classname as make_classname,
    HIDE,
)

from ...choices import image_alignment_choices
from ..bases import (
    TemplateBlock,
    TemplateBlockConfiguration,
    ToggleableBlock,
    ToggleableConfig,
)


class ImageConfiguration(TemplateBlockConfiguration, ToggleableConfig):
    alignment = blocks.ChoiceBlock(
        choices=image_alignment_choices,
        default=image_alignment_choices.default,
        required=True,
        label=_("Alignment"),
        help_text=_("The alignment of the image."),
        classname=HIDE(0, "custom_template")
    )

    class Meta:
        label = _("Configuration")
        icon = "cog"
        button_label = _("Open Settings")
        label_format = _("Image Configuration")
        absolute_position = True


class Image(ToggleableBlock, TemplateBlock):
    advanced_settings_class = ImageConfiguration

    templates = (
        ("globlocks/blocks/components/image/full.html", _("Full Width")),
        ("globlocks/blocks/components/image/small.html", _("Small")),
        ("globlocks/blocks/components/image/medium.html", _("Medium")),
        ("globlocks/blocks/components/image/large.html", _("Large")),
    )

    image = ImageChooserBlock(
        required=True,
        help_text=_("The image to display."),
    )

    class Meta:
        group=_("Images")
        label = _("Image")
        label_format = _("Image: {label}")
        icon = "image"


