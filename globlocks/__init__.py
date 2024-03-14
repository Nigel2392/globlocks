from wagtail.fields import StreamField

class GloblockField(StreamField):
    """
        A streamfield meant for keeping migration files small.
        The configuration settings for each block expand the
        size of the migration files by a lot.
    """

    def __init__(self, *args, **kwargs):
        # If we did not get an arg, pass an empty list through to the parent.
        if not args:
            args = [[]]
        return super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, _, kwargs = super().deconstruct()
        return name, path, [], kwargs




