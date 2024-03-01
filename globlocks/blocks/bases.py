from wagtail import blocks
from django.utils.translation import gettext_lazy as _

from collections import OrderedDict

class BaseBlockConfiguration(blocks.StructBlock):
    """
        Common fields each block should have,
        these blocks are hidden under the block's "Configure" dropdown.
    """

    MUTABLE_META_ATTRIBUTES = [
        "label",
        "button_label",
        "icon",
    ]

    def __init__(self, *args, base_block=None, **kwargs):
        self.base_block: BaseBlock = base_block
        super().__init__(*args, **kwargs)

    def get_translatable_segments(self, value):
        return []
    
    def restore_translated_segments(self, segments):
        pass

    def setup_for_base_block(self, base_block: "BaseBlock"):
        if self.base_block:
            raise ValueError("Configuration class instances must not be reused! <%(self_base)s> <%(base)s>" % {
                "self_base": self.base_block,
                "base": base_block,
            })
        self.base_block = base_block

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        context["verbose_name"] = self.meta.label or self.name or self.__class__.__name__
        context["button_label"] = self.meta.button_label
        context["button_icon"] = self.meta.icon
        context["full_size"] = self.meta.full
        return context

    class Meta:
        form_template = (
            "wagtailadmin/block_forms/base_block_settings_struct.html"
        )
        label = _("Configure")
        button_label = _("Open Settings")
        full=False


class BaseBlock(blocks.StructBlock):
    """
        Let the user easily configure blocks by adding custom settings.
    """
    
    MUTABLE_META_ATTRIBUTES = blocks.StructBlock.MUTABLE_META_ATTRIBUTES + [
        "block_classname",
    ]
    STYLE_TEMPLATE_VAR = "styles"
    STYLE_ATTRIBUTES = [
        "block_classname",
    ]

    # include context of settings in baseblock?
    include_settings_context = False

    # override for different advanced settings class
    advanced_settings_class = BaseBlockConfiguration

    # placeholder
    settings: BaseBlockConfiguration = blocks.Block()

    class Meta:
        block_classname = "ga-block"

    def __init__(self, local_blocks=None, **kwargs):
        local_blocks = self.init_local_blocks(local_blocks, **kwargs)
        local_blocks = self.override_local_blocks(local_blocks, **kwargs)

        for _, block in local_blocks:
            if isinstance(block, type):
                continue

            if hasattr(block, "setup_for_base_block") and isinstance(block, BaseBlockConfiguration):
                block.setup_for_base_block(self)

        self.settings = self.advanced_settings_class(
            base_block=self,
            **self.advanced_settings_kwargs(**kwargs)
        )

        local_blocks = (
            # add the settings to the local blocks so it can be used in the template
            ("settings", self.settings),
            *local_blocks,
        )

        super().__init__(local_blocks, **kwargs)

        settings = self.child_blocks.get("settings")
        if not settings:
            # logging.warning(f"Block {self.__class__.__name__} has no settings, deleting settings block.")
            delete_metaclass_block(self, "settings")
            delete_child_block(self, "settings")
        else:
            settings_children = settings.child_blocks
            if not settings_children:
                # logging.warning(f"Block {self.__class__.__name__} has no settings: {settings_children}, deleting settings block.")
                delete_metaclass_block(self, "settings")
                delete_child_block(self, "settings")

    def init_local_blocks(self, local_blocks=None, **kwargs):
        if local_blocks is None:
            local_blocks = ()
        return local_blocks
    
    def render_as_preview(self, value, context=None):
        return None

    def override_local_blocks(self, local_blocks, **kwargs):
        return local_blocks 

    def get_settings(self, value):
        return value.get("settings", {})
    
    def advanced_settings_kwargs(self, **kwargs):
        return {}

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context)
        if self.include_settings_context:
            for k, v in self.get_settings(value).items():
                context["self"][k] = v
                context[self.TEMPLATE_VAR][k] = v

        context[self.STYLE_TEMPLATE_VAR] = {}
        for k in self.STYLE_ATTRIBUTES:
            context[self.STYLE_TEMPLATE_VAR][k] = getattr(self.meta, k, None)

        return context

class BaseConfigurableBlockMeta(blocks.DeclarativeSubBlocksMetaclass):
    def __new__(mcs, name, bases, attrs):

        configurable_blocks = ()

        # Get all configurable blocks from the base classes
        for base in bases:
            if hasattr(base, "configurable_blocks"):
                configurable_blocks += base.configurable_blocks

        if "configurable_blocks" in attrs:
            configurable_blocks += attrs["configurable_blocks"]

        # Setup placeholders for the configurable blocks,
        # This is needed in case the blocks actually get included.
        for (block_name, _) in configurable_blocks:
            attrs[block_name] = blocks.Block()

        return super().__new__(mcs, name, bases, attrs)

def has_metaclass_blocks(block):
    return hasattr(block, "declared_blocks") or hasattr(block, "base_blocks")

def delete_metaclass_block(block, block_name):
    if hasattr(block, "declared_blocks"):
        if block_name in block.declared_blocks:
            del block.declared_blocks[block_name]
    if hasattr(block, "base_blocks"):
        if block_name in block.base_blocks:
            del block.base_blocks[block_name]

def delete_child_block(block, block_name):
    try:
        del block.child_blocks[block_name]
    except KeyError:
        pass

class BaseConfigurableBlock(blocks.StructBlock, metaclass=BaseConfigurableBlockMeta):
    """
        Used to create base blocks which may or may not be
        configurable by the user.
        Mainly for a better developer experience, and to
        keep the code DRY.
    """

    default_configurable = True

    # The blocks configurable by the user if the 
    # option to configure the block is enabled.
    configurable_blocks = (
        # ("block_name", BlockClass()),
    )

    # The blocks configurable by the user if the
    configurable_by_kwarg: dict[str, str] = {
        # "kwarg_name": "block_name",
        # "kwarg_name": ["block_name_1", "block_name_2"],
    }
    # kwarg_name = True | False

    # Defaults to be used if the block value gets deleted.
    defaults = {
        # "block_name": "default_value",
    }

    def __init__(self, local_blocks=None, configurable=None, configurable_local_blocks=(), *args, **kwargs):
        if local_blocks is None:
            local_blocks = ()

        if configurable is None:
            configurable = self.default_configurable

        all_blocks = self.configurable_blocks + configurable_local_blocks

        self.configured_kwargs = {}
        for (kwarg_name, block_names) in self.configurable_by_kwarg.items():
            if isinstance(block_names, str):
                block_names = (block_names,)
                
            for block_name in block_names:
                if kwarg_name in kwargs:
                    self.configured_kwargs[block_name] = bool(kwargs[kwarg_name])
                else:
                    self.configured_kwargs[block_name] = getattr(self, kwarg_name, configurable)

        for kwarg_name, _ in self.configurable_by_kwarg.items():
            if kwarg_name in kwargs:
                del kwargs[kwarg_name]

        if configurable or self.configured_kwargs:
            local_blocks += (
                *(
                    (block_name, block)
                    for (block_name, block) in (
                        all_blocks
                    ) if self.configured_kwargs.get(block_name, configurable)
                ),
            )
        else:
            # Delete relevant blocks set by the DeclarativeStructBlockMetaclass
            if has_metaclass_blocks(self):
                # Delete blocks set by 
                for (block_name, _) in all_blocks:
                    is_configured = self.configured_kwargs.get(block_name, configurable)
                    if not is_configured:
                        delete_metaclass_block(self, block_name)

        super().__init__(local_blocks, *args, **kwargs)

        # Delete blocks set by super().init
        for (block_name, _) in all_blocks:
            is_configured = self.configured_kwargs.get(block_name, configurable)
            if not is_configured:
                delete_child_block(self, block_name)

        # For later use in context
        self.configurable = configurable

    def default_context_data(self):
        """
            Default context used in the template and form.
        """
        return {
            "is_configurable": self.configurable,
            "configured_kwargs": self.configured_kwargs,
        }

    def get_form_context(self, value, prefix="", errors=None):
        context = super().get_form_context(value, prefix=prefix, errors=errors)
        context.update(self.default_context_data())
        return context
    
    def get_context(self, value, parent_context=None):
        # Initialize the context
        context = super().get_context(value, parent_context)
        context.update(
            self.default_context_data()
        )

        # If the block is configurable, there is 
        # no need to set defaults.
        if self.configurable:
            return context
        
        # Set defaults in case the block is deleted
        block_self = context.get("self", None)
        if isinstance(block_self, (blocks.StructValue, OrderedDict, dict)):
            # Set configurable here too
            block_self["is_configurable"] = self.configurable

            # # Set defaults in case the block is deleted
            for key, value in self.defaults.items():
                # Don't overwrite existing values
                if key in block_self:
                    continue

                block_self[key] = value

        return context
    
