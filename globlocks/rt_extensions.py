from django.http import HttpRequest
from django.template.response import TemplateResponse
from wagtail.admin.rich_text.editors.draftail.features import (
    EntityFeature,
    BlockFeature,
)
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineEntityElementHandler,
    BlockElementHandler,
)
from draftjs_exporter.dom import DOM
from wagtail import hooks
from wagtail.rich_text import (
    EntityHandler,
)



class SimpleInlineEntityElementHandler(InlineEntityElementHandler):
    immutability: str
    config: "SimpleRichTextFeature"

    def get_attribute_data(self, attrs):
        return self.config.get_attribute_data(attrs)


class SimpleEntityHandler(EntityHandler):
    identifier = None
    config: "SimpleRichTextFeature" = None
    
    @classmethod
    def get_db_attributes(cls, tag):
        return cls.config.get_db_attributes(tag)
    
    @classmethod
    def expand_db_attributes(cls, attrs):
        return cls.config.expand_db_attributes(attrs)


class JSTemplateMixin:
    js_template_name: str = None

    def get_js_template(self, request: HttpRequest):
        return self.js_template_name
    
    def get_js_context(self, request: HttpRequest):
        return {
            'self': self,
        }
    
    def render_js_template(self, request: HttpRequest):
        template = self.get_js_template(request)
        context = self.get_js_context(request)

        return TemplateResponse(
            request,
            template,
            context,
            status=200,
            content_type="application/javascript",
        )


class SimpleRichTextFeature:
    entity_element_handler = SimpleInlineEntityElementHandler
    entity_handler         = SimpleEntityHandler
    entity_feature         = EntityFeature

    identifier_key  = None
    identifier      = None
    tag:            str  = None
    feature_name:   str  = None
    description:    str  = None
    label:          str  = None
    icon:           str  = None
    style:          dict = None
    immutable:      bool = True

    @property
    def type_(self):
        return self.feature_name.upper()
    
    @property
    def feature_type(self):
        return self.type_
    
    @staticmethod
    def set_if(d, k, v):
        if v:
            d[k] = v
        return d
    
    def get_control(self):
        control = {
            'type':         self.feature_type,
        }

        self.set_if(control, 'label', self.label)
        self.set_if(control, 'description', self.description)
        self.set_if(control, 'icon', self.icon)
        self.set_if(control, 'element', self.tag)

        return control
    
    def decorate(self, props):
        attrs = {}
        if self.identifier_key and self.identifier:
            attrs[self.identifier_key] = self.identifier
        return DOM.create_element(self.tag, attrs, props['children'])
    
    def construct_entity_element_handler(self):
        class EntityElementHandler(self.entity_element_handler):
            config = self
            immutability = "IMMUTABLE" if self.immutable else "MUTABLE"
        return EntityElementHandler
    
    def construct_entity_handler(self):
        class EntityHandler(self.entity_handler):
            config = self
        return EntityHandler
    
    def from_database_format(self):
        from_db_tag = f"{self.tag}"
        if self.identifier:
            from_db_tag += f"[{self.identifier_key}='{self.identifier}']"
        return {
            from_db_tag: self.construct_entity_element_handler()(self.type_)
        }
    
    def to_database_format(self):
        return {}
        
    def get_attribute_data(self, attrs):
        raise NotImplementedError("get_attribute_data must be implemented")

    def get_db_attributes(self, tag):
        raise NotImplementedError("get_db_attributes must be implemented for link/embed features")
    
    def expand_db_attributes(self, attrs):
        raise NotImplementedError("expand_db_attributes must be implemented for link/embed features")
    
    def get_js_urls(self) -> list[str]:
        return None
    
    def get_css_urls(self) -> dict[str, list[str]]:
        return None


def register_simple_feature(simple_feature: SimpleRichTextFeature):

    if not isinstance(simple_feature, SimpleRichTextFeature) and not issubclass(simple_feature, SimpleRichTextFeature):
        raise ValueError("Invalid feature config type")
    
    if issubclass(simple_feature, SimpleRichTextFeature):
        simple_feature = simple_feature()

    if not simple_feature.feature_name:
        raise ValueError("Feature name must be set")
    

    if hasattr(simple_feature, "get_admin_urls"):
        hooks.register("register_admin_urls")(simple_feature.get_admin_urls)


    @hooks.register('register_rich_text_features')
    def register_feature(features):
        if simple_feature.entity_handler and simple_feature.tag == "embed":
            handler = simple_feature.construct_entity_handler()
            features.register_embed_type(handler)

        elif simple_feature.entity_handler:
            handler = simple_feature.construct_entity_handler()
            features.register_link_type(handler)

        features.register_editor_plugin(
            'draftail', simple_feature.feature_name, simple_feature.entity_feature(
                simple_feature.get_control(),
                js=simple_feature.get_js_urls(),
                css=simple_feature.get_css_urls(),
            )
        )

        features.register_converter_rule('contentstate', simple_feature.feature_name, {
            'from_database_format': simple_feature.from_database_format(),
            'to_database_format': simple_feature.to_database_format(),
        })

        features.default_features.append(simple_feature.feature_name)



class BaseAlignmentFeature(SimpleRichTextFeature):
    immutable               = False
    identifier_key          = 'class'
    tag                     = 'p'
    entity_feature          = BlockFeature
    entity_handler          = None
    entity_element_handler  = BlockElementHandler
    alignment               = None

    @property
    def feature_name(self):
        return f"align-{self.alignment}"
    
    @property
    def identifier(self):
        return f'text-{self.alignment}'
    
    def get_css_urls(self) -> dict[str, list[str]]:
        return {
            "all": ["globlocks/rt_extensions/alignment.css"]
        }
    
    def get_attribute_data(self, attrs):
        return {
            self.identifier_key: self.identifier,
        }

    def to_database_format(self):
        return super().to_database_format() | {
            'block_map': {
                self.type_: {
                    'element': self.tag,
                    'props': {
                        self.identifier_key: self.identifier,
                    }
                }
            }
        }
