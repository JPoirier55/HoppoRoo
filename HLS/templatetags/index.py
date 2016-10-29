from django import template
register = template.Library()

@register.filter
def index(List, i):
    """
    Filter - returns an index to a specified value in a list
    """
    return List[int(i)]
