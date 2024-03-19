from django.template import library

register = library.Library()

# col_size
# col_xs
# col_sm
# col_md
# col_lg
# col_xl


@register.simple_tag(name="get_from_mapping")
def do_get_from_mapping(mapping, key):
    if hasattr(mapping, "get"):
        return mapping.get(key)
    
    if hasattr(mapping, "__getitem__"):
        return mapping[key]
    
    return getattr(mapping, key)


@register.simple_tag(name="columns")
def do_columns(col_size, col_xs=None, col_sm=None, col_md=None, col_lg=None, col_xl=None):
    col_size = col_size or col_xs or col_sm or col_md or col_lg or col_xl
    col_xs = col_xs or col_size
    col_sm = col_sm or col_xs
    col_md = col_md or col_sm
    col_lg = col_lg or col_md
    col_xl = col_xl or col_lg
    return f"col-{col_size} col-xs-{col_xs} col-sm-{col_sm} col-md-{col_md} col-lg-{col_lg} col-xl-{col_xl}"


