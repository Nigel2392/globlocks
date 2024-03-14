from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from ...settings import (
    GLOBLOCKS_RICHTEXT_FEATURES_HEADINGS,
)
from ...util import (
    make_block_tuple,
)
from ..bases import (
    ToggleShowableBlock,
)



class TextBlock(ToggleShowableBlock):
    """
        A block for text.
    """
    default_features = GLOBLOCKS_RICHTEXT_FEATURES_HEADINGS
    text = blocks.Block()

    def init_local_blocks(self, local_blocks=None, **kwargs):
        features = kwargs.pop("features", self.default_features)
        return make_block_tuple(
            local_blocks,
            text=blocks.RichTextBlock(
                required=kwargs.pop("required", True),
                help_text=kwargs.pop("help_text", None),
                features=features,
                max_length=kwargs.pop("max_length", None),
                search_index=kwargs.pop("search_index", False),
                **kwargs.pop("block_kwargs", {}) or {},
            )
        )

    class Meta:
        group=_("Text")
        icon = "paragraph"
        label = _("Text")
        label_format = _("Text: {text}")
        template = "globlocks/blocks/components/text/text_block.html"

