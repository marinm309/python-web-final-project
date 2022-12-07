from django import template

register = template.Library()

@register.filter
def replace_filter(value):
    if '_' in value:
        array_of_value = value.split('_')
        result = map(lambda x: x[0].upper() + x[1:], array_of_value)
        return '/'.join(result)
    return value