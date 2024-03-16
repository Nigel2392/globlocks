from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from ... import (
    block_fields,
    bases,
)
from ...block_fields import (
    JustifyBlock,
)
from ...bases import (
    ToggleShowableConfiguration,
    ToggleShowableBlock,
)


class FlatMenuConfiguration(ToggleShowableConfiguration):
    alignment = JustifyBlock(
        choices=JustifyBlock.default_choices + (
            ("text-justify", _("Justify")),
        )
    )

    class Meta:
        icon = "list-ul"
        form_template = "globlocks/blocks/components/menus/flat/settings_form.html"

