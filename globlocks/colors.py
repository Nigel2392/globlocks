"""
    Utility module for converting colors to different formats.
    Currently supports the following formats:
    - Hexadecimal
    - RGB
    - HSL
    - RGBA
    - HSLA
"""

_default_alpha = 0

class rgb(tuple):
    def __new__(cls, r, g, b, a=_default_alpha):
        return super().__new__(cls, (r, g, b, a))

    def __str__(self):
        return f"{self.r},{self.g},{self.b}"
    
    @property
    def rgba(self):
        return f"{self.r},{self.g},{self.b},{self.a}"

    @property
    def r(self):
        return self[0]
    
    @property
    def g(self):
        return self[1]
    
    @property
    def b(self):
        return self[2]
    
    @property
    def a(self):
        return self[3] if len(self) > 3 else _default_alpha

def to_rgb(color, as_string=True, preserve_alpha=False, default_alpha=_default_alpha):
    if color.startswith("#"):
        color = from_hex(color, preserve_alpha=preserve_alpha, default_alpha=default_alpha)
    elif color.startswith("rgb"):
        color = from_rgb(color, preserve_alpha=preserve_alpha, default_alpha=default_alpha)
    elif color.startswith("hsl"):
        color = from_hsl(color, preserve_alpha=preserve_alpha, default_alpha=default_alpha)
    else:
        color = 0,0,0
        if preserve_alpha:
            color = color + (default_alpha,)
    
    if as_string:
        return ",".join(str(int(c)) for c in color)
    
    return rgb(*color)

def _p_alpha(preserve_alpha, default_alpha=_default_alpha):
    return (default_alpha,) if preserve_alpha else ()

def from_hex(color, preserve_alpha=False, default_alpha=_default_alpha):
    color = color.lstrip("#")
    if len(color) == 3:
        color = "".join([c*2 for c in color])
    elif len(color) == 6:
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4)) + _p_alpha(preserve_alpha, default_alpha)
    elif len(color) == 8:
        if preserve_alpha:
            return tuple(int(color[i:i+2], 16) for i in (0, 2, 4, 6))
        color = color[:-2]
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    else:
        raise ValueError(f"Invalid color value: {color}")
    
def from_rgb(color, preserve_alpha=False, default_alpha=_default_alpha):
    return from_color(color, "rgb", preserve_alpha=preserve_alpha, default_alpha=default_alpha)

def from_hsl(color, preserve_alpha=False, default_alpha=_default_alpha):
    return from_color(color, "hsl", preserve_alpha=preserve_alpha, default_alpha=default_alpha)
    
def from_color(color, startswith="rgb", preserve_alpha=False, default_alpha=_default_alpha):
    if color.startswith(f"{startswith}a"):
        color = color.replace(f"{startswith}a(", "").replace(")", "").split(",")
        if preserve_alpha:
            return tuple(float(c) for c in color)
        return tuple(float(c) for c in color[:3])
    
    color = color.replace(f"{startswith}(", "").replace(")", "").split(",")
    if preserve_alpha:
        return tuple(float(c) for c in color) + _p_alpha(preserve_alpha, default_alpha)
    
    return tuple(c for c in color)

