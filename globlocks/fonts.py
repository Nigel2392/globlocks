
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from globlocks.settings import (
    GLOBLOCKS_FONT_LIST,
)

class FontValue:
    def __init__(self, name=None, path=None, size=None, unit="em"):
        self._name = name
        self._path = path
        self._size = size
        self._unit = unit

    @property
    def font_name(self):
        return mark_safe(self._name)

    @property
    def font_path(self):
        return mark_safe(self._path)

    @property
    def font_size(self):
        return mark_safe(f"{self._size}{self._unit}")
    
    @property
    def fontface(self):
        return mark_safe(f"""@font-face {{
    font-family: {self.font_name};
    src: url({static(self.font_path)});
}}""")

    def _json(self):
        return {
            "name": self._name,
            "path": self._path,
            "size": self._size,
            "unit": self._unit,
        }


class Font:
    name: str
    path: str

    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def deconstruct(self):
        return (
            "{}.{}".format(self.__class__.__module__, self.__class__.__name__),
            [],
            {
                "name": self.name,
                "path": self.path,
            },
        )


FONT_LIST = GLOBLOCKS_FONT_LIST or (
    Font("Acme", "globlocks/fonts/Acme-Regular.ttf"),
    Font("Bebas Neue", "globlocks/fonts/BebasNeue-Regular.ttf"),
    Font("Caveat", "globlocks/fonts/Caveat-Regular.ttf"),
    Font("Inconsolata", "globlocks/fonts/Inconsolata-Regular.ttf"),
    Font("Inter", "globlocks/fonts/Inter-Regular.ttf"),
    Font("Kanit", "globlocks/fonts/Kanit-Regular.ttf"),
    Font("Lato", "globlocks/fonts/Lato-Regular.ttf"),
    Font("Lobster", "globlocks/fonts/Lobster-Regular.ttf"),
    Font("Manrope", "globlocks/fonts/Manrope-Regular.ttf"),
    Font("Montserrat", "globlocks/fonts/Montserrat-Regular.ttf"),
    Font("NotoSans", "globlocks/fonts/NotoSans-Regular.ttf"),
    Font("Oswald", "globlocks/fonts/Oswald-Regular.ttf"),
    Font("Pacifico", "globlocks/fonts/Pacifico-Regular.ttf"),
    Font("Permanent Marker", "globlocks/fonts/PermanentMarker-Regular.ttf"),
    Font("Phudu", "globlocks/fonts/Phudu-Regular.ttf"),
    Font("Poppins", "globlocks/fonts/Poppins-Regular.ttf"),
    Font("Roboto", "globlocks/fonts/Roboto-Regular.ttf"),
    Font("RobotoCondensed", "globlocks/fonts/RobotoCondensed-Regular.ttf"),
    Font("RobotoMono", "globlocks/fonts/RobotoMono-Regular.ttf"),
    Font("Rubik", "globlocks/fonts/Rubik-Regular.ttf"),
    Font("Rubik Iso", "globlocks/fonts/RubikIso-Regular.ttf"),
    Font("Shadows Into Light", "globlocks/fonts/ShadowsIntoLight-Regular.ttf"),
    Font("Ubuntu", "globlocks/fonts/Ubuntu-Regular.ttf"),
    Font("Zeyada", "globlocks/fonts/Zeyada-Regular.ttf"),
    Font("Alfa SlabOne", "globlocks/fonts/AlfaSlabOne-Regular.ttf"),
    Font("Amatic SC", "globlocks/fonts/AmaticSC-Regular.ttf"),
    Font("Fugaz One", "globlocks/fonts/FugazOne-Regular.ttf"),
    Font("Julius Sans One", "globlocks/fonts/JuliusSansOne-Regular.ttf"),
    Font("Lobster Two", "globlocks/fonts/LobsterTwo-Regular.ttf"),
    Font("Monoton", "globlocks/fonts/Monoton-Regular.ttf"),
    Font("Patua One", "globlocks/fonts/PatuaOne-Regular.ttf"),
    Font("Rock Salt", "globlocks/fonts/RockSalt-Regular.ttf"),
    Font("Rubik Mono One", "globlocks/fonts/RubikMonoOne-Regular.ttf"),
    Font("Sacramento", "globlocks/fonts/Sacramento-Regular.ttf"),
    Font("Stint Ultra Expanded", "globlocks/fonts/StintUltraExpanded-Regular.ttf"),
    Font("Ultra", "globlocks/fonts/Ultra-Regular.ttf"),
    Font("Victor Mono", "globlocks/fonts/VictorMono-VariableFont_wght.ttf"),
    Font("PT Mono", "globlocks/fonts/PTMono-Regular.ttf"),
    Font("Share Tech Mono", "globlocks/fonts/ShareTechMono-Regular.ttf"),
    Font("Bangers", "globlocks/fonts/Bangers-Regular.ttf"),
    Font("Space Mono", "globlocks/fonts/SpaceMono-Regular.ttf"),
    Font("Creepster", "globlocks/fonts/Creepster-Regular.ttf"),
    Font("Philosopher", "globlocks/fonts/Philosopher-Regular.ttf"),
)

FONT_LIST = sorted(FONT_LIST, key=lambda font: font.name)

def get_default_font():
    return {
        "name": FONT_LIST[0].name,
        "path": FONT_LIST[0].path,
        "size": 1,
        "unit": "em",
    }

DefaultFontFamily = FONT_LIST[0]
DefaultFontFamily.__call__ = get_default_font
