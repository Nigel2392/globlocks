from wagtail.admin.panels import FieldPanel
from .widgets import ColorInputWidget

class NativeColorPanel(FieldPanel):
    def widget_overrides(self):
        # For Wagtail<3.0 we use widget_overrides
        return {
            self.field_name: ColorInputWidget(),
        }

    def get_form_options(self):
        # For Wagtail 3.0 we use get_form_options
        # So we can mix them to provide supports to Wagtail 2,3
        opts = super().get_form_options()
        opts["widgets"] = self.widget_overrides()
        return opts
