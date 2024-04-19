from django.template import library, TemplateSyntaxError
from django.urls import reverse
from django.http import HttpRequest
from django.utils.safestring import mark_safe
from wagtail.models import Page, PAGE_TEMPLATE_VAR

register = library.Library()


MIN_SIZE = 1
MAX_SIZE = 6

@register.simple_tag(name="class")
def class_tag(*args) -> str:
    """
        Helper tag for joining classes together.
    """
    return " ".join(args)

@register.filter(name="add_class")
def add_class(value: str, adder: str) -> str:
    """
        Helper tag for adding a class to an element.
    """
    if not value:
        raise TemplateSyntaxError("add_class tag requires a value")

    return f"{value} {adder}"

@register.filter(name="heading")
def heading(value: str, adder: int) -> str:
    """
        Helper tag for altering heading sizes, taking into account the min and max heading sizes.
    """
    if not value:
        raise TemplateSyntaxError("heading tag requires a value")

    if isinstance(value, str) and value.startswith("h"):
        value = value[1:]
        
    try:
        value = int(value)
    except ValueError:
        raise TemplateSyntaxError("heading tag requires a number")
        
    value += adder
    
    if value < MIN_SIZE:
        value = MIN_SIZE
    elif value > MAX_SIZE:
        value = MAX_SIZE

    return f"h{value}"


# EDIT_ICON = """<svg xmlns="http://www.w3.org/2000/svg" width="{}" height="{}" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
#     <!-- The MIT License (MIT) -->
#     <!-- Copyright (c) 2011-2024 The Bootstrap Authors -->
#     <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
#     <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
# </svg>"""
# 
# 
# @register.simple_tag(name="edit_icon", takes_context=True)
# def edit_icon(context, size=24, block_id = None):
#     if not block_id and "block_id" not in context:
#         return ""
#     
#     if not block_id:
#         block_id = context["block_id"]
# 
#     if (
#         not context\
#         or not "request" in context\
#         or not PAGE_TEMPLATE_VAR in context
#     ):
#         return ""
#     
#     request: HttpRequest = context["request"]
#     page: Page = context[PAGE_TEMPLATE_VAR]
# 
#     if not( 
#             request.user.is_authenticated\
#             or request.user.has_perm("wagtailadmin.access_admin")\
#             and request.user.has_perm(
#                 f"{page.content_type.app_label}.change_{page.content_type.model}",
#             )
#         ):
#         return ""
#     
#     base_edit_url = context.get(
#         "page_base_edit_url",
#     )
#     if not base_edit_url:
#         base_edit_url = reverse(
#             "wagtailadmin_pages:edit",
#             args=[page.id],
#         )
#         context["page_base_edit_url"] = base_edit_url
#     
#     edit_url = f"{base_edit_url}#block-{block_id}-section"
#     icon = EDIT_ICON.format(size, size)
#     return mark_safe(f'<a href="{edit_url}" class="globlocks-edit-icon">{icon}</a>')
# 