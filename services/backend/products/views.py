from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, CarouselItem, Category, FilterGroup, Favorite

def catalog(request, category_slug=None):
    """Каталог товаров"""
    products = Product.objects.select_related('category').prefetch_related('filters').all().order_by('-created_at')
    
    current_category = None
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Фильтры цены (пока по рознице, для простоты)
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        products = products.filter(price_retail__gte=min_price)
    
    if max_price:
        products = products.filter(price_retail__lte=max_price)

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

    # --- ВАЖНО: Считаем цену для отображения ---
    for product in products:
        product.display_price = product.get_price_for_user(request.user)

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
    product = get_object_or_404(Product, id=product_id)
    
    # Считаем цену
    product.display_price = product.get_price_for_user(request.user)
    
    related_products = []
    if product.category:
        qs = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        for p in qs:
            p.display_price = p.get_price_for_user(request.user)
        related_products = qs

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        favorite.delete()
        
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))