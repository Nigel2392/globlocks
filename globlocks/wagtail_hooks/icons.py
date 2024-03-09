from wagtail import hooks


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        "globlocks/icons/text-align/text-left.svg",
        "globlocks/icons/text-align/text-center.svg",
        "globlocks/icons/text-align/text-right.svg",
    ]