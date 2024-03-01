from django.db import models
from django.utils.translation import gettext_lazy as _


class ColorField(models.CharField):
    description = _("Color Input Field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 255
        super().__init__(*args, **kwargs)
