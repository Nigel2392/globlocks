from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .bases import BaseBlockConfiguration, BaseBlock


class TemplateBlockConfiguration(BaseBlockConfiguration):
    # placeholder, real value get set in __init__()
    custom_template = blocks.Block()

    def __init__(self, local_blocks=None, template_choices=None, classname=None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        # We don't want to reveal any unnecessary information to the user.
        template_choices = [(str(i), label) for i, (value, label) in enumerate(template_choices)]
        local_blocks += (
            (
                "custom_template",
                blocks.ChoiceBlock(
                    choices=template_choices,
                    default=template_choices[0][0],
                    required=True,
                    label=_("Template"),
                    help_text=_("The template to use for rendering."),
                    classname=classname,
                    translatable=False,
                ),
            ),
        )

        super().__init__(local_blocks, **kwargs)

class TemplateBlock(BaseBlock):

    advanced_settings_class = TemplateBlockConfiguration,

    templates = (
        ("", _("Default")),
    )

    def advanced_settings_kwargs(self, **kwargs):
        kwargs = super().advanced_settings_kwargs(**kwargs)
        kwargs["template_choices"] = (
            *self.templates,
        )
        return kwargs
    
    def clean(self, value):
        value = super().clean(value)
        settings = value["settings"]
        if "custom_template" in settings:
            template_choice = settings["custom_template"]
            try: 
                template_choice = int(template_choice)
            except ValueError:
                raise ValidationError(_("Invalid template choice (Not an integer)."))
            
            try:
                _ = self.templates[template_choice]
            except IndexError:
                raise ValidationError(_("Invalid template choice (Out of bounds)."))
            
        return value

    def get_template(self, value=None, context=None):
        settings = value["settings"]
        if "custom_template" in settings:
            template_choice = settings["custom_template"]
            try: 
                template_choice = int(template_choice)
            except ValueError:
                return super().get_template(value=value, context=context)
            
            try: 
                template = self.templates[template_choice][0]
            except IndexError:
                return super().get_template(value=value, context=context)

            if template:
                return template
            
        return super().get_template(value=value, context=context)


