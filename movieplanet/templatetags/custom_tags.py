from django import template

register = template.Library()

@register.filter
def plusify(value):
    return value.replace(' ', '+')