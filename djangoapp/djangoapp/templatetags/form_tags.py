from django.template import Library

register = Library()


@register.simple_tag()
def label_tag(field, **attrs):
    """ A simple template tag to enable attributes to be specified when rendering the label tag of
         a form field.
     """
    return field.label_tag(attrs=attrs)
