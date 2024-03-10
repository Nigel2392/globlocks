from django import template
from django.template import library
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.conf import settings

from globlocks.preview import PreviewUnavailable, preview_of_block
from globlocks import staticfiles


INDENT = getattr(settings, "GLOBLOCKS_SCRIPT_INDENT", "        ")


register = library.Library()


@register.simple_tag(name="render_as_preview", takes_context=True)
def render_as_preview(context, block, fail_silently=False, **kwargs):
    try:
        v = preview_of_block(block, context, fail_silently=fail_silently, **kwargs)
        if v is None:
            return ""
        return v
    except PreviewUnavailable:
        return block




def format_static_file(file):

    for prefix in ["/", "http://", "https://"]:
        if file.startswith(prefix):
            return file

    return static(file)


@register.simple_tag(name="globlocks_js")
def globlocks_js():
    s = []
    for js in staticfiles.globlocks_js:
        if hasattr(js, "__html__"):
            s.append(js.__html__())
        else:
            s.append(f'<script src="{format_static_file(js)}"></script>')
    return mark_safe(f"\n{INDENT}".join(s))


@register.simple_tag(name="globlocks_css")
def globlocks_css():
    s = []
    for css in staticfiles.globlocks_css:
        if hasattr(css, "__html__"):
            s.append(css.__html__())
        else:
            s.append(f'<link rel="stylesheet" href="{format_static_file(css)}">')
    return mark_safe(f"\n{INDENT}".join(s))


class FragmentNode(template.Node):
    """
        This comes from wagtail.admin.templatetags.wagtailadmin_tags
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
        if settings.DEBUG:
            raise template.TemplateSyntaxError(error_message)
        return ""

    stripped = "stripped" in options

    return FragmentNode(nodelist, target_var, stripped=stripped)
