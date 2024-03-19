from django.utils.translation import gettext_lazy as _

class list_default(list):
    def __init__(self, *args, default=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = default

    @property
    def default(self):
        if callable(self._default):
            default = self._default()
        else:
            default = self._default

        if default is None:
            default = self[0][0]

        return default
    

# text_alignment_choices = list_default([
#     ("text-left", "Left"),
#     ("text-center", "Center"),
#     ("text-right", "Right"),
# ], default="text-left")
text_alignment_choices = list_default([
    ("left", _("Left")),
    ("center", _("Center")),
    ("right", _("Right")),
], default="left")

image_alignment_choices = list_default([
    ("left", _("Left")),
    ("center", _("Center")),
    ("right", _("Right")),
], default="left")



