from django.db.models.fields import CharField


class LowerCaseCharField(CharField):
    """ Override CharField to convert to lowercase before saving. """

    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
