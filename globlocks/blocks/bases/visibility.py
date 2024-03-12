from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from .baseblock import BaseBlock, BaseBlockConfiguration

class ToggleShowableConfiguration(BaseBlockConfiguration):
    is_shown = blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Show"),
        help_text=_("Whether to show the content."),
        classname="col-12",
    )

    class Meta:
        label = _("Configuration")
        icon = "cog"
        button_label = _("Open Settings")


class ToggleShowableBlock(BaseBlock):
    advanced_settings_class = ToggleShowableConfiguration

    class Meta:
        icon = "arrow-up"
        label = _("Toggle Showable")

    def render(self, value, context=None):
        settings = self.get_settings(value)
        if not settings.get("is_shown"):
            return ""
        return super().render(value, context)
