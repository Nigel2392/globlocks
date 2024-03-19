from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

from globlocks.settings import GLOBLOCKS_RICHTEXT_FEATURES
from .text import (
    TextBlock,
)
from ..block_fields import (
    OrderableBlock,
    Orderable,
)



class ImageTextBlockConfiguration(TextBlock.advanced_settings_class):

    ordering = OrderableBlock(
        required=True,
        help_text=_("The order of the image and text."),
        orderables=[
            Orderable(
                "globlocks/blocks/components/image_text/image.html",
                label=_("Image"),
                name="image",
            ),
            Orderable(
                "globlocks/blocks/components/image_text/text.html",
                label=_("Text"),
                name="text",
            ),
        ],
    )

    class Meta:
        label = _("Layout Settings")
        button_label = _("Open Layout Settings")
        label_format = _("Image Text Layout Settings")
        hide_labels = False
        absolute_position = True
        icon = "resubmit"


class ImageTextBlock(TextBlock):
    default_features = GLOBLOCKS_RICHTEXT_FEATURES
    advanced_settings_class = ImageTextBlockConfiguration

    image = ImageChooserBlock(
        required=True,
        help_text=_("The image to display."),
    )

    heading = blocks.CharBlock(
        required=True,
        help_text=_("The heading above the text."),
    )


    class Meta:
        label = _("Image and Text")
        label_format = _("Image / Text: {heading} {image}")
        group = _("Images")
        template = "globlocks/blocks/components/image_text/image_text.html"
        form_template = "globlocks/blocks/components/image_text/image_text_form.html"
        compact_view = True

    def render_as_preview(self, value, context=None):
        return mark_safe(f"<strong>{value['heading']}:</strong> {strip_tags(value['text'])}\n")

