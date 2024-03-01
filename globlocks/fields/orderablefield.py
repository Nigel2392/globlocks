from typing import Any
from django.db import models
from django.db.models import Model
from django.utils.functional import cached_property
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django import forms
import json

from ..util import AutoJSONEncoder
from ..widgets import OrderableWidget

class Orderable:
    __name = None
    label = None
    value = None

    def __init__(self, value: str, label: str = None, name=None):
        if not label:
            raise ValueError("Label must be specified")
        self.__name = name or slugify(label)
        self.label = label
        self.value = value

    def __str__(self):
        return self.label
    
    def __html__(self):
        return self.label

    def __repr__(self):
        return f"Orderable({self.label}, {self.value})"

    @property
    def name(self):
        return self.__name

    def json(self):
        return {
            "name": str(self.name),
            "label": str(self.label),
            "value": str(self.value),
        }

    def deconstruct(self):
        return (
            "{0}.{1}".format(self.__class__.__module__, self.__class__.__name__),
            [],
            {
                "name": self.name,
                "label": self.label,
                "value": self.value,
            },
        )


class OrderableFormField(forms.JSONField):
    def __init__(self, orderables=None, *args, **kwargs):
        self.orderables = orderables
        kwargs["encoder"] = AutoJSONEncoder
        super().__init__(*args, **kwargs)

    def prepare_value(self, value: Any) -> Any:
        if isinstance(value, list):
            return json.dumps(value, cls=AutoJSONEncoder)
        return value

    def to_python(self, value: Any) -> Any:
        value = super().to_python(value)
        return value
    
    # @property
    # def widget(self):
    #     return OrderableWidget(orderables=self.orderables, encoder=self.encoder)


class OrderableField(models.JSONField):
    def __init__(self, orderables=list[Orderable] or callable, *args, **kwargs):
        self.orderables = self.filter_orderables(orderables)
        self.encoder = AutoJSONEncoder
        super().__init__(*args, **kwargs)

    def filter_orderables(self, orderables):
        if callable(orderables):
            orderables = orderables()
        for i, orderable in enumerate(orderables):
            if isinstance(orderable, Orderable):
                orderables[i] = orderable
            elif isinstance(orderable, tuple):
                orderables[i] = Orderable(**orderable[2])
            else:
                raise ValueError(
                    "Orderables must be a list of Orderable objects or tuples"
                )
        return orderables

    def from_db_value(self, value, expression, connection) -> Any:
        value = super().from_db_value(value, expression, connection)
        orderables = []
        # field is a list of list[orderable.value]
        if isinstance(value, list):
            for orderable in value:
                orderables.append(self.get_orderable(orderable))

        # field is a list[orderable.value]
        elif isinstance(value, str):
            orderables.append(self.get_orderable(value))
        return orderables

    def get_prep_value(self, value: Any) -> Any:
        if isinstance(value, list):
            return [orderable.value for orderable in value]
        return value

    @cached_property
    def _get_default(self):
        return lambda: [orderable.value for orderable in self.orderables]

    def validate(self, value: Any, model_instance: Model) -> None:
        super().validate(value, model_instance)
        if not isinstance(value, list):
            raise ValidationError("OrderableField must be a list")
        for orderable in value:
            if not self.get_orderable(orderable):
                raise ValidationError(f"Orderable {orderable} does not exist")

    def get_orderable(self, value):
        for orderable in self.orderables:
            if orderable.value == value:
                return orderable
        return None

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "widget": OrderableWidget(
                    orderables=self.orderables,
                ),
                "form_class": OrderableFormField,
                **kwargs,
            }
        )

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["orderables"] = [
            orderable.deconstruct() for orderable in self.orderables
        ]
        return name, path, args, kwargs
