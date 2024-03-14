from django.template import Library


register = Library()

_LEFT = -1
_CENTER = 0
_RIGHT = 1

class _Position:
    def __init__(self, position: int=_CENTER):
        self.position = position

    def __str__(self):
        if self.position == _LEFT:
            return "left"
        if self.position == _CENTER:
            return "center"
        if self.position == _RIGHT:
            return "right"
        return "center"
    
    def __int__(self):
        return self.position
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.position == other
        if isinstance(other, _Position):
            return self.position == other.position
        if isinstance(other, str):
            return str(self) == other
        return False
    
    def __gt__(self, other):
        if isinstance(other, int):
            return self.position > other
        if isinstance(other, _Position):
            return self.position > other.position
        return False
    
    def __lt__(self, other):
        if isinstance(other, int):
            return self.position < other
        if isinstance(other, _Position):
            return self.position < other.position
        return False
    
    def __ge__(self, other):
        if isinstance(other, int):
            return self.position >= other
        if isinstance(other, _Position):
            return self.position >= other.position
        return False
    
    def __le__(self, other):
        if isinstance(other, int):
            return self.position <= other
        if isinstance(other, _Position):
            return self.position <= other.position
        return False
    
Left = _Position(_LEFT)
Center = _Position(_CENTER)
Right = _Position(_RIGHT)

@register.filter(name="position_is")
def position_is(blocks, counter) -> _Position:
    if not blocks:
        return Center
    length = len(blocks)
    if length == 1:
        return Center
    elif length == 2:
        return Left if counter == 0 else Right
    half = length / 2
    if counter < half:
        return Left
    if counter > half:
        return Right
    return Center

@register.simple_tag(name="position_of", takes_context=True)
def position_of(context, blocks) -> _Position:
    fl = context.get("forloop", {})
    counter0 = fl.get("counter0", 0)
    return position_is(blocks, counter0)



