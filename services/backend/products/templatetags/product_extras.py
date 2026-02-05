from django import template

register = template.Library()

@register.filter
def get_list_from_query(query_dict, key):
    """
    Возвращает список значений для ключа из request.GET.
    Пример использования: request.GET|get_list_from_query:'filter_1'
    """
    return query_dict.getlist(f"filter_{key}")