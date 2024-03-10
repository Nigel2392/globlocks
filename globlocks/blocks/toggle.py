from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from .bases import BaseBlockConfiguration, BaseBlock


class ToggleableBlockConfiguration(BaseBlockConfiguration):
    is_shown = blocks.BooleanBlock(
        label=_("Show"),
        help_text=_("Show or hide the block to the users."),
        required=False,
        default=True,
    )

    class Meta:
        label = _("Toggleable")
        button_label = _("Toggleable Settings")
        hide_labels = False
        full=False


class ToggleableBlock(BaseBlock):
    """
        A block that can be toggled on or off.
        Configuration blocks must inherit from ToggleableBlockConfiguration!
    """
    advanced_settings_class = ToggleableBlockConfiguration


    def render(self, value, context=None):
        settings = self.get_settings(value)
        if not settings.get("is_shown", True):
            return ""
        return super().render(value, context)
    
    

