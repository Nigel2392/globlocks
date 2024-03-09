from django.utils.translation import gettext_lazy as _
from wagtail.admin.rich_text.editors.draftail.features import (
    ControlFeature,
)
from wagtail import hooks

from globlocks.rt_extensions import (
    BaseAlignmentFeature,
    register_simple_feature,
)



class AlignLeftFeature(BaseAlignmentFeature):
    # label                   = "⮜"
    icon                    = 'text-left'
    description             = _('Align Left')
    alignment               = 'left'


class AlignCenterFeature(BaseAlignmentFeature):
    # label                   = "⬤"
    icon                    = 'text-center'
    description             = _('Align Center')
    alignment               = 'center'


class AlignRightFeature(BaseAlignmentFeature):
    # label                   = "⮞"
    icon                    = 'text-right'
    description             = _('Align Right')
    alignment               = 'right'


@hooks.register('register_rich_text_features')
def register_word_counter(features):

    feature_name = 'word-counter'
    features.default_features.append(feature_name)
    features.register_editor_plugin(
        'draftail',
        feature_name,
        ControlFeature({
                'type': feature_name,
            },
            js=['globlocks/rt_extensions/word-counter.js'],
        )
    )

register_simple_feature(AlignLeftFeature)
register_simple_feature(AlignCenterFeature)
register_simple_feature(AlignRightFeature)
