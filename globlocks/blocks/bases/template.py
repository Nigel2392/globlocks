from wagtail import blocks
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

from .baseblock import BaseBlockConfiguration, BaseBlock

from conditional_field import (
    classname as make_classname,
    handler,
)


class TemplateBlockConfiguration(BaseBlockConfiguration):
    # placeholder, real value get set in __init__()
    custom_template = blocks.Block()

    def __init__(self, local_blocks=None, template_choices=None, classname=None, **kwargs):
        if not local_blocks:
            local_blocks = ()

        if not template_choices:
            raise ValueError("template_choices is required.")

        template_choices = tuple(template_choices)
        local_blocks += (
            (
                "custom_template",
                blocks.ChoiceBlock(
                    choices=template_choices,
                    default=template_choices[0][0],
                    required=True,
                    label=_("Template"),
                    help_text=_("The template to use for rendering."),
                    classname=make_classname(
                        classname,
                        handler("custom_template"),
                    ),
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
        kwargs["template_choices"] = self.templates_choices
        return kwargs
    
    def __init__(self, local_blocks=None, **kwargs):
        self.templates_dict = {}
        self.templates_choices = []

        # We don't want to reveal any unnecessary information to the user.
        # We will define a dictionary of user-friendly values to use in the
        # advanced settings form.
        for i, data in enumerate(self.templates):
            if len(data) == 2:
                key, (template, label) = i, data
            elif len(data) == 3:
                key, template, label = data
            else:
                raise ValueError("Invalid `templates` attribute.")
            
            self.templates_choices.append((str(key), label))
            self.templates_dict[str(key)] = template
        
        super().__init__(local_blocks, **kwargs)
    
    def clean(self, value):
        value = super().clean(value)
        settings = value["settings"]
        if "custom_template" in settings:
            template_choice = settings["custom_template"]

            try:
                _ = self.templates_dict[str(template_choice)]
            except KeyError:
                raise ValidationError(
                    message=_("Invalid template choice (KeyError)."),
                )
            
        return value

    def get_template(self, value=None, context=None):
        settings = value["settings"]

        if "custom_template" in settings:
            template_choice = settings["custom_template"]

            try: 
                template = self.templates_dict[str(template_choice)]
            except KeyError:
                return super().get_template(value=value, context=context)

            if template:
                return template
            
        return super().get_template(value=value, context=context)


