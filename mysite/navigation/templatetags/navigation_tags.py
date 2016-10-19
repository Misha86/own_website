from django import template
from navigation.models import MenuItem

register = template.Library()

# context - бере інформацію з сторінки на якій розміщений тег і передає в шаблон тегу

# @register.inclusion_tag('navigation.html', takes_context=True)
# def navigation_menu(context, *args, **kwargs):
#     navigation ={}
#     navigation['hello'] = context['user']
#     navigation['profile'] = kwargs['profile']
#     navigation['name'] = args[0]
#     return navigation


@register.inclusion_tag('../templates/navigation/navigation.html', takes_context=True)
def navigation_menu(context, *args, **kwargs):
    navigation = {}
    path = kwargs['path']
    menu = MenuItem.objects.all().order_by('menu_number')
    navigation['menu'] = menu
    navigation['path'] = path
    return navigation

