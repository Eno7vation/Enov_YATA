from django import template

register = template.Library()


@register.filter
def sub(value, arg1):
    return value - arg1