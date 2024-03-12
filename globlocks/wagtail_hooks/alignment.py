from django.utils.translation import gettext_lazy as _
from django.utils.html import json_script
from draftjs_exporter.dom import DOM
from draftjs_exporter.defaults import render_children
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    Block,
    BLOCK_KEY_NAME,
    BlockElementHandler,
)
from wagtail.admin.rich_text.editors.draftail.features import (
    ControlFeature,
)
from wagtail import hooks
from globlocks import util


@hooks.register('insert_global_admin_js')
def global_admin_js():
    # For translating alignments in the Draftail editor
    # See rt_extensions/alignment.js
    return json_script({
            "left": _("Align Left"),
            "center": _("Align Center"),
            "right": _("Align Right"),
        },
        "globlocks-text-alignment-i18n",
    )

def text_alignment_elem(tag_name):
    """
        A utility function for creating elements with the
        data-alignment attribute set.
    """
    def text_alignment(props):

        if "block" in props and "data" in props["block"]:
            alignment = props["block"]["data"].get("alignment", "left")
            return DOM.create_element(
                tag_name,
                {
                    "data-alignment": alignment,
                    "class": f"text-{alignment}",
                },
                render_children(props),
            )

        return DOM.create_element(
            tag_name,
            {"data-alignment": "left"},
            render_children(props),
        )
    
    return text_alignment


def _new_alignment_handler(tag_name, block_type):
    return {
        f"{tag_name}[data-alignment='left']": AlignmentHandler(block_type),
        f"{tag_name}[data-alignment='center']": AlignmentHandler(block_type),
        f"{tag_name}[data-alignment='right']": AlignmentHandler(block_type),
    }



class AlignmentBlock(Block):
    """
        Block for persisting data-alignment attribute.
        The data attribute is omitted by default.
    """
    def __init__(self, typ, depth=0, key=None, alignment=None):
        super().__init__(typ, depth, key)
        self.data = {"alignment": alignment or "left"}

    def as_dict(self):
        return super().as_dict() | {
            "data": self.data,
        }



class AlignmentHandler(BlockElementHandler):
    """
    Draft.js block handler for alignment blocks.
    """

    mutability = "MUTABLE"
    
    def create_block(self, name, attrs, state, contentstate):
        return AlignmentBlock(
            self.block_type, depth=state.list_depth, key=attrs.get(BLOCK_KEY_NAME),
            alignment=attrs.get("data-alignment", "left"),
        )



_BLOCK_TYPES = (
    ("unstyled", "p"),
    ("header-one", "h1"),
    ("header-two", "h2"),
    ("header-three", "h3"),
    ("header-four", "h4"),
    ("header-five", "h5"),
    ("header-six", "h6"),
    ("blockquote", "blockquote"),
    ("code-block", "pre"),
)



@hooks.register('register_rich_text_features')
def register_richtext_alignment_features(features):
    feature_name = "text-alignment"

    # Register the control feature (plugin is also included in the JS)
    features.default_features.append(feature_name)
    features.register_editor_plugin(
        "draftail",
        feature_name,
        ControlFeature({
                "type": feature_name,
            },
            js=[
                "globlocks/richtext/alignment/alignment.js",
            ],
            css={"all": ["globlocks/richtext/alignment/alignment.css"]},
        ),
    )

    block_map = {}
    from_db_format = {}

    for block_type, tag_name in _BLOCK_TYPES:
        block_map[block_type] = text_alignment_elem(tag_name)
        from_db_format.update(
            _new_alignment_handler(tag_name, block_type)
        )

    for fn in util.get_hooks('register_block_types'):
        block_map, from_db_format = fn(block_map, from_db_format)

    config = {
        "to_database_format": {
            "block_map": block_map,
        },
        "from_database_format": from_db_format,
    }

    for fn in util.get_hooks('construct_alignment_config'):
        config = fn(config)

    features.register_converter_rule('contentstate', feature_name, config)
