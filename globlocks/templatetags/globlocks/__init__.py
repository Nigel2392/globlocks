from typing import Any, Union
from django import template
from django.urls import reverse
from django.http import HttpRequest
from django.template import library
from django.utils.safestring import mark_safe
from django.templatetags.static import static

from wagtail.models import Page
from wagtail.documents.models import AbstractDocument
from wagtail.images.models import (
    AbstractImage,
    AbstractRendition,
)

from globlocks.preview import PreviewUnavailable, preview_of_block
from globlocks.settings import GLOBLOCKS_SCRIPT_INDENT, GLOBLOCKS_DEBUG
from globlocks.staticfiles import (
    globlocks_js as staticfiles_globlocks_js,
    globlocks_css as staticfiles_globlocks_css,
)
from globlocks.util import (
    get_hooks,
)
from globlocks.blocks import (
    components,
)

import re


register = library.Library()


def format_static_file(file):

    for prefix in ["/", "http://", "https://"]:
        if file.startswith(prefix):
            return file

    return static(file)


@register.simple_tag(name="render_as_preview", takes_context=True)
def render_as_preview(context, block, fail_silently=False, **kwargs):
    try:
        v = preview_of_block(block, context, fail_silently=fail_silently, **kwargs)
        if v is None:
            return ""
        return v
    except PreviewUnavailable:
        return block


def base_script_tag(files_or_hook, hook_name, format_fn) -> callable:
    def _tag(context):
        request = context.get("request", None)
        
        s = []

        files = files_or_hook
        files = (
            *files,
            *get_hooks(hook_name),
        )

        for file in files:
            if callable(file):
                file = file(request, context)

            if hasattr(file, "__html__"):
                s.append(file.__html__())
            else:
                s.append(format_fn(file))

        return mark_safe(f"\n{GLOBLOCKS_SCRIPT_INDENT}".join(s))
    return _tag

def format_script_tag(file):
    return f'<script src="{format_static_file(file)}"></script>'

def format_css_tag(file):
    return f'<link rel="stylesheet" href="{format_static_file(file)}">'

globlocks_js_hook_name = "globlocks_js"
register.simple_tag(name=globlocks_js_hook_name, takes_context=True)(
    base_script_tag(staticfiles_globlocks_js, globlocks_js_hook_name, format_script_tag)
)

globlocks_css_hook_name = "globlocks_css"
register.simple_tag(name=globlocks_css_hook_name, takes_context=True)(
    base_script_tag(staticfiles_globlocks_css, globlocks_css_hook_name, format_css_tag)
)


HAS_PROTO_RE = re.compile(r"^[a-zA-Z0-9]+://")
POSSIBLE_LINK_TYPES = Union[
    components.LinkValue,
    Page, AbstractDocument,
    str, Any,
]


@register.simple_tag(name="link", takes_context=True)
def do_link(context, value: POSSIBLE_LINK_TYPES, full: bool = False) -> str:
    request: HttpRequest = context.get("request", None)

    if isinstance(value, components.LinkValue):
        return value.get_url(request, full=full)

    elif isinstance(value, Page):
        if full:
            return value.get_full_url(request)
        return value.get_url(request)

    elif isinstance(value, AbstractImage):
        rendition: AbstractRendition = value.get_rendition("original")
        if full:
            return request.build_absolute_uri(rendition.url)
        return rendition.url
    
    elif hasattr(value, "get_absolute_url"):
        return value.get_absolute_url(request)
    
    elif hasattr(value, "url"):
        if full:
            return request.build_absolute_uri(value.url)
        return value.url

    elif isinstance(value, str):
        if full and not any([
            value.startswith("//"),
            HAS_PROTO_RE.match(value),
        ]):
            return request.build_absolute_uri(value)

        return value

    for hook in get_hooks("generate_link"):
        result = hook(value, context, full=full)
        if result:
            return result
        
    return value


class FragmentNode(template.Node):
    """
        This generously comes from wagtail.admin.templatetags.wagtailadmin_tags
    """

    def __init__(self, nodelist, target_var, stripped=False):
        self.nodelist = nodelist
        self.target_var = target_var
        self.stripped = stripped

    def render(self, context):
        fragment = self.nodelist.render(context) if self.nodelist else ""
        # Only strip the leading and trailing spaces, unlike
        # {% blocktrans trimmed %} that also does line-by-line stripping.
        # Then, use mark_safe because the SafeString returned by
        # NodeList.render() is lost after stripping.
        if self.stripped:
            fragment = mark_safe(fragment.strip())
        context[self.target_var] = fragment
        return ""


@register.tag(name="block_fragment")
def fragment(parser, token):
    """
    Store a template fragment as a variable.

    Usage:
        {% fragment as header_title %}
            {% blocktrans trimmed %}Welcome to the {{ site_name }} Wagtail CMS{% endblocktrans %}
        {% endfragment %}

    Copy-paste of slippers’ fragment template tag.
    See https://github.com/mixxorz/slippers/blob/254c720e6bb02eb46ae07d104863fce41d4d3164/slippers/templatetags/slippers.py#L173.

    To strip leading and trailing whitespace produced in the fragment, use the
    `stripped` option. This is useful if you need to check if the resulting
    fragment is empty (after leading and trailing spaces are removed):

        {% fragment stripped as recipient %}
            {{ title }} {{ first_name }} {{ last_name }}
        {% endfragment }
        {% if recipient %}
            Recipient: {{ recipient }}
        {% endif %}

    Note that the stripped option only strips leading and trailing spaces, unlike
    {% blocktrans trimmed %} that also does line-by-line stripping. This is because
    the fragment may contain HTML tags that are sensitive to whitespace, such as
    <pre> and <code>.
    """
    error_message = "The syntax for fragment is {% fragment as variable_name %}"

    try:
        tag_name, *options, target_var = token.split_contents()
        nodelist = parser.parse(("endblock_fragment",))
        parser.delete_first_token()
    except ValueError:
        if GLOBLOCKS_DEBUG:
            raise template.TemplateSyntaxError(error_message)
        return ""

    stripped = "stripped" in options

    return FragmentNode(nodelist, target_var, stripped=stripped)
