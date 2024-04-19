import copy
from typing import Any, Callable
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from wagtail.documents.blocks import DocumentChooserBlock
from django import forms
from django.core.validators import RegexValidator
from wagtail import blocks

from ..utils import (
    CharBlockWithAttrs,
    URLBlockWithAttrs,
    EmailBlockWithAttrs,
)

from conditional_field import (
    SHOW, handler,
)



class _LinkChoice:
    def __init__(self,
            value:              Any,
            label:              str,
            url_getter:         Callable[[Any], str],
            text_getter:        Callable[[Any], str],
            block:              blocks.Block,
        ):
        self.value = value
        self.label = label
        self.url_getter = url_getter
        self.text_getter = text_getter
        self.block = block

    def __str__(self):
        return str(self.label)

    def __iter__(self):
        return iter([self.value, self.label])

    def get_text(self, value):
        return self.text_getter(value)
    
    def get_url(self, value):
        return self.url_getter(value)


class _LinkChoices:
    def __init__(self, link_choices: list[_LinkChoice]):
        self.choices = []
        self.url_getters: dict[str, Callable[[Any], str]] = {}
        self.text_getters: dict[str, Callable[[Any], str]] = {}
        self._link_choices = link_choices
        self.link_choices = {
            choice.value: choice
            for choice in link_choices
        }
        for choice in link_choices:
            self.choices.append((choice.value, choice.label))
            self.url_getters[choice.value] = choice.url_getter
            self.text_getters[choice.value] = choice.text_getter

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._link_choices[key]
        
        return self.link_choices[key]

    def get_text(self, choice, value):
        return self.text_getters[choice](value)
    
    def get_url(self, choice, value, request = None, full = False):
        return self.url_getters[choice](value, request, full)


def get_page_url(value, request = None, full = False):
    if full:
        return value.get_full_url(request)
    return value.get_url(request)


def get_document_url(value, request = None, full = False):
    if full:
        return request.build_absolute_uri(value.url)
    return value.url

def get_external_url(value, request = None, full = False):
    return value

def get_email_url(value, request = None, full = False):
    return f"mailto:{value}"

def get_phone_url(value, request = None, full = False):
    return f"tel:{value}"


link_choices = _LinkChoices([
    _LinkChoice(
        "page", _("Page"),
        get_page_url,
        lambda value: value.title,
        blocks.PageChooserBlock(
            required=False,
            label=_("Page"),
        )
    ),
    _LinkChoice(
        "document", _("Document"),
        get_document_url,
        lambda value: value.title,
        DocumentChooserBlock(
            required=False,
            label=_("Document"),
        )
    ),
    _LinkChoice(
        "external", _("External Link"),
        get_external_url,
        lambda value: value,
        URLBlockWithAttrs(
            required=False,
            label=_("External Link"),
            attrs={
                "placeholder": _("https://example.com"),
                "autocomplete": "off",
            },
        )
    ),
    _LinkChoice(
        "email", _("Email Link"),
        get_email_url,
        lambda value: value,
        EmailBlockWithAttrs(
            required=False,
            label=_("Email"),
            attrs={
                "placeholder": _("john@example.com"),
                "autocomplete": "off",
            },
        )
    ),
    _LinkChoice(
        "phone", _("Tel"),
        get_phone_url,
        lambda value: value,
        CharBlockWithAttrs(
            required=False,
            label=_("Tel"),
            attrs={
                "placeholder": _("123-456-7890"),
                "autocomplete": "off",
            },
            validators=[
                RegexValidator(
                    regex=r"^\+?[0-9\-\s\(\)]+$",
                    message=_("Enter a valid phone number."),
                )
            ],
            min_length=7,
            max_length=14,
        )
    ),
])


class LinkValue(blocks.StructValue):
    @property
    def link_text(self):
        text = self.get("text", None)
        if text:
            return text
        
        chosen = self.get("choice", None)
        value = self.get(chosen, None)
        if not value:
            return None
        
        return link_choices.get_text(chosen, value)

    @property
    def link_url(self):
        chosen = self.get("choice", None)
        value = self.get(chosen, None)
        if not value:
            return None
        
        return link_choices.get_url(chosen, value)

    def get_url(self, request: HttpRequest, full: bool = False):
        chosen = self.get("choice", None)
        value = self.get(chosen, None)
        if not value:
            return None
                
        return link_choices.get_url(chosen, value, request, full)


class Link(blocks.StructBlock):
    # Allowed features for the link.
    ALLOWED_FEATURES = [i.value for i in link_choices]

    # Control some styling inside of the wagtailadmin
    MUTABLE_META_ATTRIBUTES = [
        "stacked",
        "no_row_padding",
    ]

    # (Optional) text for the link.
    text = CharBlockWithAttrs(
        required=False,
        label=_("Text"),
        max_length=255,
        attrs={
            "placeholder": _("A short description of the link (optional)"),
            "autocomplete": "off",
        },
    )

    # Placeholder for the choice block
    choice = blocks.Block()

    def __init__(self, local_blocks = None, features = None, conditional_widget = forms.RadioSelect, *args, **kwargs):
        if local_blocks is None:
            local_blocks = ()

        if not features:
            features = self.ALLOWED_FEATURES

        block_features = []
        url_block_choices = []
        for feature in features:
            if feature not in self.ALLOWED_FEATURES:
                raise ValueError(f"Invalid feature: {feature}")

            feature = link_choices[feature]
            block_features.append(feature)
            url_block_choices.append(
                (feature.value, feature.label)
            )

        local_blocks += (
            ("choice", blocks.ChoiceBlock(
                required=True,
                choices=url_block_choices,
                default=features[0],
                label=_("Link Type"),
                classname=handler("choice"),
                widget=conditional_widget,
            )),
        )

        if len(features) == 1:
            raise ValueError("Link must have at least two features, use a regular block instead.")

        self.features = features
        self.block_features: list[_LinkChoice] = block_features
        
        super().__init__(local_blocks, *args, **kwargs)

        for feature in self.block_features:
            # Deepcopy the block - just in case.
            block = feature.block
            block = copy.deepcopy(block)
            block.set_name(feature.value)

            # Automatically generate a new classname for the block for the conditional field.
            classname = block._constructor_args[1].pop("classname", None)
            choice_class = SHOW(feature.value, "choice")
            if classname:
                classname = f"{choice_class} {classname}"
            else:
                classname = choice_class

            # Set the classname in the constructor args and metaclass.
            block._constructor_args[1]["form_classname"] = classname
            setattr(block.meta, "form_classname", classname)

            self.child_blocks[feature.value] = block

    class Meta:
        stacked = True
        no_row_padding = True
        value_class = LinkValue
        label_format = _("Link: {text}")
        label = _("Link")
        icon = "link"
        form_template = (
            "globlocks/blocks/components/link/form.html"
        )


    def clean(self, value):
        # Validate the value based on the choice picked.
        value = super().clean(value)
        chosen = value.get("choice", None)
        v = value.get(chosen, None)
        if not v:
            raise blocks.StructBlockValidationError(block_errors={
                chosen: forms.ValidationError(
                    _("This field is required."),
                    code="required",
                )
            })

        return value
