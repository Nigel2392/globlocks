from django.template import library, TemplateSyntaxError

register = library.Library()


MIN_SIZE = 1
MAX_SIZE = 6


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
