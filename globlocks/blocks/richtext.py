from typing import Union
from wagtail import blocks
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from globlocks.blocks import (
    toolbar,
)
from globlocks.blocks import (
    ColorBlock,
)
from globlocks.blocks import (
    BaseBlock,
    BaseBlockConfiguration,
    AttributeConfiguration,
)



class BaseBlockTextConfiguration(AttributeConfiguration):
    class_name = blocks.CharBlock(
        required=False,
        label=_("Class Name"),
        translatable=False,
    )

    class Meta:
        icon = "edit"
        form_template = "globlocks/blocks/richtext/settings_form.html"


    def get_attributes(self, value, context=None):
        return {
            "class": [
                value.get("class_name", ""),
            ],
        }


class HeadingConfiguration(BaseBlockTextConfiguration):
    toolbar = toolbar.ToolbarBlock(
        tag_name="h2",
        targets="text",
        required=False,
        label=_("Toolbar"),
        tools=[
            "BOLD",
            "ITALIC",
            "UNDERLINE",
            "STRIKETHROUGH",
            "JUSTIFY_LEFT",
            "JUSTIFY_CENTER",
            "JUSTIFY_RIGHT",
            # "HEADING_1",
            "HEADING_2",
            "HEADING_3",
            "HEADING_4",
            "HEADING_5",
            "HEADING_6",
            "COLOR",
            "BACKGROUND_COLOR",
        ]
    )

    class Meta:
        form_template = "globlocks/blocks/richtext/heading_settings_form.html"
        label_format = '{heading_level}'

    def get_attributes(self, value, context=None):
        attrs = super().get_attributes(value, context)
        return attrs
    
class HeadingValue(blocks.StructValue):
    class Meta:
        icon = "title"
        label = _("Heading")
        button_label = _("Heading Settings")
    
    @property
    def heading_tag(self):
        return f"h{self.get('settings').get('heading_level', 2)}"


class HeadingElement(BaseBlock):
    advanced_settings_class = HeadingConfiguration

    text = blocks.CharBlock(
        required=True,
        label=_("Text"),
    )

    class Meta:
        icon = "title"
        label = _("Heading")
        template = "globlocks/blocks/richtext/heading.html"
        form_template = "globlocks/blocks/richtext/text_and_settings_form.html"
        value_class = HeadingValue
        hide_help_text = True
        label_format = '{settings}: {text}'


class RichTextElementConfiguration(BaseBlockTextConfiguration):
    color_bg = ColorBlock(
        label=_("Background Color"),
        required=False,
    )

    color_text = ColorBlock(
        label=_("Text Color"),
        required=False,
    )

    class Meta:
        form_template = "globlocks/blocks/richtext/text_settings_form.html"

    def get_attributes(self, value, context=None):
        attrs = super().get_attributes(value, context)
        attrs["style"] = [
            ("--color-bg", value.get("color_bg", "")),
            ("--color-text", value.get("color_text", "")),
        ]
        return attrs

class RichTextElement(BaseBlock):
    always_add_features = [
        'align-left',
        'align-center',
        'align-right',
        'word-counter',
    ]
    disallowed_features = [
        "h1", "h2", "h3", "h4", "h5", "h6",
    ]
    advanced_settings_class = RichTextElementConfiguration

    text = blocks.Block()

    def init_local_blocks(self, local_blocks=None, **kwargs):
        features = kwargs.pop("features", None)

        if not features:
            features = []

        if self.disallowed_features:
            for feature in self.disallowed_features:
                if feature in features:
                    features.remove(feature)

        if self.always_add_features:
            for feature in self.always_add_features:
                if feature not in features:
                    features.append(feature)

        local_blocks = super().init_local_blocks(local_blocks, **kwargs)
        local_blocks += (
            ("text", blocks.RichTextBlock(
                features=features,
                label=_("Text"),
            )),
        )
        return local_blocks

    class Meta:
        icon = "doc-full"
        label = _("Text")
        template = "globlocks/blocks/richtext/richtext.html"
        form_template = "globlocks/blocks/richtext/text_and_settings_form.html"
        hide_help_text = True


class RichTextBlock(blocks.StructBlock):

    blocks = blocks.Block()

    def __init__(self, local_blocks=None, features=None, min_num: int = 1, max_num: int = None, block_counts: dict = None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        local_blocks = tuple(local_blocks)
        local_blocks += (
            ("heading", HeadingElement()),
            ("text", RichTextElement(features=features)),
        )

        local_blocks = (
            ("blocks", blocks.StreamBlock(
                local_blocks,
                label=_("Text Blocks"),
                min_num=min_num,
                max_num=max_num,
                block_counts=block_counts or {},
            )),
        )

        super().__init__(local_blocks, **kwargs)

    class Meta:
        icon = "list-ul"
        label = _("Rich Text")
        template = "globlocks/blocks/richtext/listblock.html"


