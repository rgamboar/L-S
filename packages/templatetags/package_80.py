from django import template
register = template.Library()

@register.inclusion_tag('print_80.html')
def show_print_80(package):
    return {'package': package}