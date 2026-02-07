from django import template
from products.models import Favorite

register = template.Library()

@register.filter
def get_list_from_query(query_dict, key):
    """
    Возвращает список значений для ключа из request.GET.
    Пример использования: request.GET|get_list_from_query:'filter_1'
    """
    return query_dict.getlist(f"filter_{key}")

@register.simple_tag(takes_context=True)
def is_favorite(context, product):
    request = context['request']
    if not request.user.is_authenticated:
        return False
    return Favorite.objects.filter(user=request.user, product=product).exists()