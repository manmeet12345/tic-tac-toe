from django import template

register = template.Library()

@register.filter
def get_item(value, key):
    try:
        return value[key]
    except (KeyError, IndexError, TypeError):
        return None