from typing import Any, TYPE_CHECKING, Tuple
from collections import defaultdict

if TYPE_CHECKING:
    from .bar import ToolbarValue

from django.utils.safestring import mark_safe



class Attribute:

    def __init__(self, name: str, separator: str = " ", multiple: bool = False):
        self.name = name
        self.separator = separator
        self.multiple = multiple
        self.values: set[str] = set()

    def __contains__(self, value: str) -> bool:
        return value in self.values
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, {self.values})"

    def has(self, value: str) -> bool:
        return value in self

    def add(self, value: str):
        if not isinstance(value, (list, tuple)) and self.multiple:
            value = [value]

        if self.multiple:
            for v in value:
                self.values.add(v)

        else:
            self.values = set([value])

    def remove(self, value: str):
        if self.has(value) and self.multiple:
            self.values.remove(value)
        else:
            self.values = set()

    def render(self) -> str:
        return f'{self.name}="{self.separator.join([str(v) for v in self.values])}"'
    
    def __str__(self):
        return self.render()


class StyleAttribute(Attribute):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.values: dict[str, list[str]] = defaultdict(list)

    def add(self, name: str, value: str):
        self.values[name].append(value)
        
    def remove(self, name: str, value: str = None):
        if value is None and name in self.values:
            del self.values[name]
        else:
            l = self.values[name]
            if value in l:
                l.remove(value)
        
    def has(self, name: str, value: str = None) -> bool:
        if value is None:
            return name in self.values
        return value in self.values[name]

    def render(self) -> str:
        s = []
        for name, values in self.values.items():
            if values:
                s.append(f"{name}: {' '.join(values)}")
        return f'''style="{';' .join(s)}"'''

class Attributes:
    def __init__(self):
        self.attrs: dict[str, Attribute] = {}
    
    def __getitem__(self, key: str) -> Attribute:
        if key not in self.attrs:
            self.attrs[key] = create_attribute(key)
        return self.attrs[key]
    
    def __setitem__(self, key: str, value: Attribute):
        if not isinstance(value, Attribute):
            value = create_attribute(key, value)
        self.attrs[key] = value

    def __delitem__(self, key: str):
        del self.attrs[key]

    def __iter__(self):
        return iter(self.attrs.values())
    
    def __str__(self):
        return " ".join([str(attr) for attr in self])
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.attrs.values()})"
    
    def render(self) -> str:
        return " ".join([str(attr) for attr in self])
    
    def add(self, name: str, *args, **kwargs):
        self[name].add(*args, **kwargs)

    def remove(self, name: str, value: str):
        self[name].remove(value)

    def has(self, name: str, *args, **kwargs):
        return self[name].has(*args, **kwargs)
    


SPECIAL_ATTRS = {
    "class": {
        "options": {
            "multiple": True,
            "separator": " ",
        },
    },
    "style": {
        "class": StyleAttribute,
    },
}

def create_attribute(name: str, value: Any = None) -> "Attribute":
    if name in SPECIAL_ATTRS:
        options = SPECIAL_ATTRS[name].get("options", {})
        cls = SPECIAL_ATTRS[name].get("class", Attribute)
        return cls(name, **options)
    return Attribute(name)


class ElementType:
    def __init__(self, toolbar: "ToolbarValue", tag: str, value: dict[str, Any]):
        self.toolbar = toolbar
        self.tag = tag
        self.value = value
        self.attrs = Attributes()

    def generate(self) -> Tuple[str, Attributes]:
        return (self.tag, self.attrs)
    
    def render_text(self, text: str):
        tag, attrs = self.generate()
        return mark_safe(f"<{tag} {attrs}>{text}</{tag}>")
    

