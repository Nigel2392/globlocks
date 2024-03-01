from django.db import models as django_models
import json

class AutoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj is django_models.NOT_PROVIDED:
            return None
        try:
            return obj._json()
        except AttributeError:
            try:
                return obj.json()
            except AttributeError:
                try:
                    return super().default(obj)
                except Exception as e:
                    raise Exception(f"Could not serialize {obj} to JSON") from e
