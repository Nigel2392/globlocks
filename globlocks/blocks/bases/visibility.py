from collections import OrderedDict
import random

from django import forms
from django.http import HttpRequest
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.functional import cached_property

from wagtail.models import (
    PAGE_TEMPLATE_VAR,
    Page,
)
from wagtail.telepath import register
from wagtail.blocks.struct_block import (
    StructBlockAdapter,
)
from wagtail import blocks

from .baseblock import BaseBlock, BaseBlockConfiguration
from globlocks.settings import (
    GLOBLOCKS_EDITORS_SEE_HIDDEN,
)


_alphabet = "abcdefghijklmnopqrstuvwxyz"

def rand_id():
    return "".join(
        random.choice(_alphabet)
        for _ in range(8)
    )


class ToggleShowableButton:
    name:  str          = None
    block: blocks.Block = None

    def get_translations(self):
        return {}
    
    def value_for_value_class(self, value):
        return value
    
    def is_shown(self, value):
        return not not value
    
    def get_js(self):
        return []
    
    def get_css(self):
        return []


class ToggleShowableButtonIsShown(ToggleShowableButton):
    name = "is_shown"

    block = blocks.BooleanBlock(
        default=True,
        required=False,
        label=_("Show"),
        help_text=_("Whether to show the content."),
        classname="col-12",

    )

    def get_translations(self):
        return super().get_translations() | {
            "showText": _("Show"),
            "hideText": _("Hide"),
        }
    
    def get_js(self):
        return super().get_js() + [
            "globlocks/admin/toggleable-block/toggleable-block-buttons.js",
        ]
    

class DateFromToBaseBlock(ToggleShowableButton):
    def is_shown(self, value):
        if not value:
            return True
        
        return super().is_shown(value) and self.op(value)
    
    def get_cmp(self):
        return timezone.now()
    
    def op(self, value):
        raise NotImplementedError("op must be implemented in a subclass")
    

class DateTimeFromButton(DateFromToBaseBlock):
    name = "hide_before_date"

    block = blocks.DateTimeBlock(
        required=False,
        blank=True,
        label=_("Visible From"),
        help_text=_("The date from which to show the content."),
        classname="col-12 col-md-6",
    )

    def op(self, value):
        return value < self.get_cmp()
    

class DateTimeToButton(DateFromToBaseBlock):
    name = "hide_after_date"

    block = blocks.DateTimeBlock(
        required=False,
        blank=True,
        label=_("Visible To"),
        help_text=_("The date until which to show the content."),
        classname="col-12 col-md-6",
    )

    def op(self, value):
        return value > self.get_cmp()
    

class ToggleableConfigValue(blocks.StructValue):
    def __init__(self, block, *args):
        super().__init__(block, *args)
        settings = self.get("settings", {})
        for button in block.buttons:
            settings[button.name] = button.value_for_value_class(
                settings.get(button.name),
            )

class ToggleableConfig(BaseBlockConfiguration):
    def __init__(self, local_blocks=None, buttons=None, *args, **kwargs):
        super().__init__(local_blocks, *args, **kwargs)

        self.buttons = buttons or []
        child_blocks = OrderedDict()
        for button in self.buttons:

            button.block.set_name(button.name)
            child_blocks[button.name] = button.block

        self.child_blocks = child_blocks | self.child_blocks
        self.hide_block_button = len(self.child_blocks) == len(self.buttons)

    def get_form_context(self, value, prefix="", errors=None):
        return super().get_form_context(value, prefix, errors) | {
            "hide_block_button": self.hide_block_button,
        }

    class Meta:
        label = _("Configuration")
        icon = "cog"
        button_label = _("Open Settings")


class ToggleableAdapter(StructBlockAdapter):
    js_constructor = "globlocks.blocks.ToggleableBlock"

    def __init__(self, block: "ToggleableBlock") -> None:
        super().__init__()
        self.block = block

    @cached_property
    def media(self):
        structblock_media = super().media
        js = set()
        css = set()

        for button in self.block.buttons:
            js.update(button.get_js())
            css.update(button.get_css())
        
        m = forms.Media(
            js=[
                *structblock_media._js,
                'globlocks/admin/toggleable-block/toggleable-block.js',
                *js,
            ],
            css={
                'all': [
                    'globlocks/admin/toggleable-block/toggleable-block.css',
                    *css,
                ],
            } 
        )
        
        return m
    
    def js_args(self, block):
        block_name, child_blocks, meta = super().js_args(block)
        buttons = {}

        for button in self.block.buttons:
            buttons[button.name] = {
                "translations": button.get_translations(),
                "label": button.block.label,
            }

        meta["buttons"] = buttons

        return block_name, child_blocks, meta


class ToggleableBlock(BaseBlock):
    advanced_settings_class = ToggleableConfig
    adapter_class = ToggleableAdapter
    buttons: list[ToggleShowableButton] = [
        DateTimeFromButton(),
        DateTimeToButton(),
        ToggleShowableButtonIsShown(),
    ]

    class Meta:
        icon = "arrow-up"
        show_text = _("Show")
        hide_text = _("Hide")

    def __init__(self, local_blocks=None, buttons=None, **kwargs):
        self.buttons = buttons or self.buttons
        super().__init__(local_blocks, **kwargs)

    def advanced_settings_kwargs(self, **kwargs):
        return super().advanced_settings_kwargs(**kwargs) | {
            "local_blocks": None,
            "buttons": self.buttons,
        }

    def render(self, value, context=None):
        settings: dict = self.get_settings(value)
        is_shown = True

        for button in self.buttons:
            is_shown = is_shown and button.is_shown(
                settings.get(button.name),
            )
        
            if not is_shown:

                if not GLOBLOCKS_EDITORS_SEE_HIDDEN:
                    return ""
                
                if not context:
                    return ""
                
                if not "request" in context\
                    or not PAGE_TEMPLATE_VAR in context:
                    return ""
                
                request: HttpRequest = context["request"]
                page: Page = context[PAGE_TEMPLATE_VAR]

                if not request.user.is_authenticated:
                    return ""
                
                if not( 
                        request.user.has_perm("wagtailadmin.access_admin")\
                        and request.user.has_perm(
                            f"{page.content_type.app_label}.change_{page.content_type.model}",
                        )
                    ):
                    return ""
                
                title = self.hidden_editor_title(value, context)
                label = self.hidden_editor_label(value, context)
                preview = self.hidden_editor_preview(value, context)
                id = rand_id()
                _js = f"javascript:(() => {{{id}.remove(); return void(0)}})()"

                # Default values, always shown
                s = [
                    f"<div class='globlocks-toggleable-block' id=\"{id}\">\n",
                    f"    <h2 class=\"mb-1\">{title}</h2>\n",
                    f"    <h3 class=\"mb-1\">({label})</h3>\n",
                ]

                # add preview when available
                if preview:
                    s.append("   <p>")
                    s.append(str(preview))
                    s.append("   </p>\n")

                # Add optional edit link
                edit_url = reverse(
                    "wagtailadmin_pages:edit",
                    args=(page.id,),
                )
                if "block_id" in context:
                    edit_url += f"#block-{context['block_id']}-section"

                s.append(
                    f"    <a href=\"{edit_url}\" class=\"globlocks-toggleable-block-btn\">{str(_('Edit'))}</a>\n"
                )
                s.append(
                    f"    <a href=\"{_js}\" class=\"globlocks-toggleable-block-btn\">{str(_('Close'))}</a>\n"
                )

                # Close container
                s.append("</div>")

                return mark_safe("".join(s))

        
        return super().render(value, context)
    
    def hidden_editor_title(self, value, context=None):
        """
            The title to be shown when the content is hidden.
            This is only shown to editors.
        """
        return str(_("This content is hidden."))
    
    def hidden_editor_label(self, value, context=None):
        """
            The label to be shown when the content is hidden.
            This is only shown to editors.
        """
        return str(self.meta.label)
    
    def hidden_editor_preview(self, value, context=None):
        """
            The preview to be shown when the content is hidden.
            This is only shown to editors.
        """
        return self.render_as_preview(value, context)
    
    @classmethod
    def register_adapter(cls, adapter = None, **kwargs):
        if adapter is None:
            adapter = cls.adapter_class(cls, **kwargs)

        if isinstance(adapter, type):
            adapter = adapter(**kwargs)

        register(adapter, cls)
        return adapter
    


ToggleableBlock.register_adapter()

