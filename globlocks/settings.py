from django.conf import settings
from django.utils.translation import gettext_lazy as _


"""
    Debug mode for the globlocks application.
    Means extra errors could be raised; more information logged etc.
"""
GLOBLOCKS_DEBUG = getattr(settings, "GLOBLOCKS_DEBUG", settings.DEBUG)


"""
    Short length filler text to be used throughout the application.
"""
LOREM_IPSUM_SHORT = getattr(settings,
    "GLOBLOCKS_LOREM_IPSUM_SHORT",
    _("Lorem ipsum dolor sit amet, consectetur adipiscing elit."),
)


"""
    Medium length filler text to be used throughout the application.
"""
LOREM_IPSUM_MEDIUM = getattr(settings,
    "GLOBLOCKS_LOREM_IPSUM_MEDIUM",
    _("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
      "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."),
)


"""
    Long length filler text to be used throughout the application.
"""
LOREM_IPSUM_LONG = getattr(settings,
    "GLOBLOCKS_LOREM_IPSUM_LONG",
    _("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
      "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
      "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
      "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
      "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
)


"""
    Font list to be used inside of the fontpicker widget/block.
"""
GLOBLOCKS_FONT_LIST = getattr(settings, "GLOBLOCKS_FONT_LIST", None)

"""
    Toolbar styles (bold, text-decoration, etc...) will use classes to style the element when rendering.
"""
GLOBLOCKS_TOOLSTYLES_ADD_CLASSES = getattr(settings, "GLOBLOCKS_TOOLSTYLES_ADD_CLASSES", True)


"""
    The indent to be used for links/scripts when generated from the helper templatetag.
"""
GLOBLOCKS_SCRIPT_INDENT = getattr(settings, "GLOBLOCKS_SCRIPT_INDENT", "        ")


"""
    Basic richtext features used throughout the application.
    Only contains inline elements.
"""
GLOBLOCKS_RICHTEXT_FEATURES = getattr(settings, "GLOBLOCKS_RICHTEXT_FEATURES", [
    "bold", "italic",
    "link", "document-link", "image", 
    'text-alignment', 'word-counter',
])


"""
    More advanced richtext features used throughout the application.
    Contains block level elements.
"""
GLOBLOCKS_RICHTEXT_FEATURES_HEADINGS = getattr(settings, "GLOBLOCKS_RICHTEXT_FEATURES_HEADINGS", [
    "h2", "h3", "h4", "h5", "bold", "italic", "ol", "ul", 
    "blockquote", "mark", "link", "document-link", "image",
    
    'text-alignment', 'word-counter',
])


"""
    This means you have to be careful with caches.
    
    Editors will see the hidden content, but the public will not.

    If you have a cache that is shared between editors and the public,
    you could end up with a situation where the public sees the hidden content.
"""
GLOBLOCKS_EDITORS_SEE_HIDDEN = getattr(settings, "GLOBLOCKS_EDITORS_SEE_HIDDEN", True)
