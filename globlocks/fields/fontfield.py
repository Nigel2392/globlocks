from typing import Any
from django.db import models
from django.db.models import Model
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError

from ..widgets import FontPickerWidget
from ..fonts import FontValue
from ..util import AutoJSONEncoder


class FontField(models.JSONField):
    """
    A field that allows the user to select a font from a list of fonts
    It also allows the user to set the size of the font
    """

    def __init__(
        self,
        fonts=None,
        preview_text=None,
        size=1,
        unit="em",
        min=0.1,
        max=100,
        stepping=0.1,
        *args,
        **kwargs,
    ):
        self.fonts = fonts
        self.measurement_unit: str = unit
        self.size = size
        self.min = min
        self.max = max
        self.stepping = stepping
        self.preview_text = preview_text
        kwargs["default"] = kwargs.pop("default", dict)
        kwargs["encoder"] = kwargs.get("encoder", AutoJSONEncoder)

        if self.fonts and not isinstance(self.fonts, tuple, list):
            raise ValueError("Fonts must be a tuple or list of Font objects")

        super().__init__(*args, **kwargs)

    def from_db_value(self, value: Any, expression: Any, connection: Any) -> Any:
        value = super().from_db_value(value, expression, connection)
        if not value:
            return value
        return FontValue(
            **value, **{"unit": self.measurement_unit} if "unit" not in value else {}
        )

    @cached_property
    def _get_default(self):
        if callable(self.default):
            return self.default
        return lambda: self.default
    
    def get_prep_value(self, value: Any) -> Any:
        if isinstance(value, FontValue):
            return {
                "name": value._name,
                "path": value._path,
                "size": value._size,
                "unit": value._unit,
            }
        return value

    def validate(self, value: Any, model_instance: Model) -> None:
        ret = super().validate(value, model_instance)

        if isinstance(value, FontValue):
            return ret

        if not value.get("name", None):
            raise ValidationError("Font name is required")
        if not value.get("path", None):
            raise ValidationError("Font path is required")
        if not value.get("size", None):
            raise ValidationError("Font size is required")

        return ret

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["fonts"] = self.fonts
        kwargs["default"] = self.default
        kwargs["size"] = self.size
        kwargs["unit"] = self.measurement_unit
        kwargs["min"] = self.min
        kwargs["max"] = self.max
        kwargs["stepping"] = self.stepping
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "widget": FontPickerWidget(
                    preview_text=self.preview_text,
                    fonts=self.fonts,
                    encoder=self.encoder,
                    unit=self.measurement_unit,
                    min=self.min,
                    max=self.max,
                    stepping=self.stepping,
                ),
                "decoder": self.decoder,
                "encoder": self.encoder,
                **kwargs,
            }
        )
