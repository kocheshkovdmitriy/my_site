from django import template

register = template.Library()

@register.simple_tag()
def get_checked(pk, list_pk):
    return 'checked' if str(pk) in list_pk else ''