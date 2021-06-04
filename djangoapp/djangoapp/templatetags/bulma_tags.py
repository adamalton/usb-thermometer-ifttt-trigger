from django.template import Library

register = Library()


@register.filter
def bulma_message_class(tags):
    """ Translate the django.contrib.messages tag(s) into a Bulma CSS class name. """
    tags_str = str(tags)
    mapping = {
        "error": "has-background-danger has-text-white",
        "warning": "has-background-warning",
        "info": "has-background-info has-text-white",
    }
    classes = []
    for tag, css_class in mapping.items():
        if tag in tags_str:
            classes.append(css_class)
    return " ".join(classes)
