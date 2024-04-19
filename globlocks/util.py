from typing import Optional, Tuple, TypeVar
from django.db import models as django_models
from wagtail import (
    blocks,
    hooks,
)
import json

class AutoJSONEncoder(json.JSONEncoder):
    """
        Helper JSON encoder class that can serialize objects that have a _json method.
        Used mostly in blocks and widgets.
    """
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
                    raise Exception(f"Could not serialize {obj} ({type(obj)}) to JSON") from e
                

def get_hooks(hook_name: str):
    """
        Helper function to get hooks from the wagtail hooks registry.
        Namespaced to the globlocks app.
    """
    return hooks.get_hooks(f'globlocks.{hook_name}')



_BLOCK_TUPLE = TypeVar("_BLOCK_TUPLE", bound=Tuple[Tuple[str, blocks.Block]])


def make_block_tuple(local_blocks: Optional[_BLOCK_TUPLE] = None, needs_initial: bool = False, **blocks: blocks.Block) -> Tuple[_BLOCK_TUPLE, _BLOCK_TUPLE]:
    """
        Helper function to create a tuple of blocks from a kwargs;

        This is useful for overriding the `__init__` method
        of your own custom block to add attributes to sub-blocks.
    """

    initial = local_blocks or ()

    if not local_blocks:
        local_blocks = ()

    local_blocks = tuple(local_blocks)

    for k, v in blocks.items():
        local_blocks += (
            (k, v),
        )

    if needs_initial:
        return local_blocks, initial
    
    return local_blocks
