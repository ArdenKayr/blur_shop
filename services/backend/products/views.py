from django.shortcuts import render, get_object_or_404
from .models import Product, CarouselItem, Category, FilterGroup
from django.db.models import Q
from .models import Product, Category, Favorite

def catalog(request, category_slug=None):
    """
    Оптимизированный каталог.
    """
    
    # --- ОПТИМИЗАЦИЯ (БЫЛО -> СТАЛО) ---
    # Мы сразу подгружаем 'category' и 'filters', чтобы не делать 100500 запросов в цикле
    products = Product.objects.select_related('category').prefetch_related('filters').all().order_by('-created_at')
    
    # 2. Категория
    current_category = None
    if category_slug:
        # Здесь тоже используем select_related не обязательно, но get_object_or_404 работает быстро
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # 3. Поиск
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # 4. Цена (Pro vs Retail)
    is_pro = request.user.is_authenticated and request.user.status == 'approved'
    price_field = 'price_pro' if is_pro else 'price_retail'

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(**{f"{price_field}__gte": min_price})
    
    if max_price:
        products = products.filter(**{f"{price_field}__lte": max_price})

    # 5. Динамические фильтры
    # Тут тоже оптимизация: prefetch_related('values') загружает значения сразу
    filter_groups = FilterGroup.objects.prefetch_related('values').all()
    selected_filters = []

    for group in filter_groups:
        param_name = f"filter_{group.id}"
        values_list = request.GET.getlist(param_name)
        
        if values_list:
            values_ids = [int(v) for v in values_list if v.isdigit()]
            if values_ids:
                products = products.filter(filters__id__in=values_ids).distinct()
                selected_filters.extend(values_ids)

    # Слайдер (он легкий, но сортировку оставим)
    carousel_items = CarouselItem.objects.all().order_by('order')

    context = {
        'carousel_items': carousel_items,
        'products': products,
        'current_category': current_category,
        'search_query': search_query,
        'filter_groups': filter_groups,
        'selected_filters': selected_filters,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'products/catalog.html', context)


def product_detail(request, product_id):
    """Страница одного товара"""
    # Ищем товар по ID. Если нет — выдаст ошибку 404 (Страница не найдена)
    product = get_object_or_404(Product, id=product_id)
    
    # Можно добавить "Похожие товары" (например, из той же категории)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def toggle_favorite(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    # Если лайк есть — удаляем, если нет — создаем
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
        
    # Возвращаем пользователя на ту же страницу, где он был
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))