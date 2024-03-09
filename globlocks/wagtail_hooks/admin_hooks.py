from wagtail import hooks
from django.templatetags.static import static
from django.utils.html import format_html

@hooks.register('insert_global_admin_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('globlocks/admin/layout.css')
    )


@hooks.register('insert_global_admin_js')
def editor_js():
    return format_html(
        '<script src="{}"></script>',
        static('globlocks/admin/block_settings.js')
    )
