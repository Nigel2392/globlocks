from wagtail import hooks


@hooks.register("register_icons")
def register_icons(icons):
    return icons + [
        # Toolbar
        "globlocks/icons/toolbar/text-bold.svg",
        "globlocks/icons/toolbar/text-h1.svg",
        "globlocks/icons/toolbar/text-h2.svg",
        "globlocks/icons/toolbar/text-h3.svg",
        "globlocks/icons/toolbar/text-h4.svg",
        "globlocks/icons/toolbar/text-h5.svg",
        "globlocks/icons/toolbar/text-h6.svg",
        "globlocks/icons/toolbar/text-italic.svg",
        "globlocks/icons/toolbar/text-strikethrough.svg",
        "globlocks/icons/toolbar/text-underline.svg",
        "globlocks/icons/toolbar/text-palette.svg",
        "globlocks/icons/toolbar/text-palette-fill.svg",

        # Justify Widget / Toolbar
        "globlocks/icons/text-align/text-left.svg",
        "globlocks/icons/text-align/text-center.svg",
        "globlocks/icons/text-align/text-right.svg",
    ]