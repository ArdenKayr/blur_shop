from django.shortcuts import render
from .models import Product, CarouselItem # <--- Добавили импорт

def catalog(request):
    products = Product.objects.all()
    # Получаем только активные слайды, отсортированные по порядку
    carousel_items = CarouselItem.objects.filter(is_active=True) 
    
    is_pro = False
    if request.user.is_authenticated:
        if hasattr(request.user, 'status') and request.user.status == 'approved':
            is_pro = True

    context = {
        'products': products,
        'carousel_items': carousel_items, # <--- Передаем в шаблон
        'is_pro': is_pro,
    }
    return render(request, 'products/catalog.html', context)