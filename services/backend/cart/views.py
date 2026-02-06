from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    """Обработчик кнопки 'Добавить в корзину'"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

def cart_remove(request, product_id):
    """Удаление товара"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

# --- НОВАЯ ФУНКЦИЯ ---
@require_POST
def cart_update(request, product_id):
    """Обновление количества товара (ввод числа или кнопки +/-)"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем число из input
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        # override_quantity=True означает "Установи ровно это число"
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        # Если ввели 0 или меньше, удаляем товар
        cart.remove(product)
        
    return redirect('cart_detail')

def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    
    total_price = 0
    is_pro = request.user.is_authenticated and request.user.status == 'approved'

    for item in cart:
        product = item['product']
        price = product.price_pro if is_pro else product.price_retail
        
        item['price'] = price
        item['total_price'] = price * item['quantity']
        
        total_price += item['total_price']

    return render(request, 'cart/detail.html', {'cart': cart, 'total_price': total_price})