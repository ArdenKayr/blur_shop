from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
        
    return redirect('cart_detail')

def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    total_price = 0

    # Пересчитываем цены
    for item in cart:
        product = item['product']
        current_price = product.get_price_for_user(request.user)
        
        item['price'] = current_price
        item['total_price'] = current_price * item['quantity']
        
        total_price += item['total_price']

    return render(request, 'cart/detail.html', {'cart': cart, 'total_price': total_price})