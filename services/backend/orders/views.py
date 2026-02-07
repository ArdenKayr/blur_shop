from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tinkoff import TinkoffPayment
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def order_create(request):
    """Страница оформления заказа"""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('catalog')

    # --- ДОБАВЛЕННЫЙ БЛОК: Подсчет цен для отображения ---
    total_price = 0
    is_pro = request.user.is_authenticated and request.user.status == 'approved'

    # Пробегаемся по корзине и считаем актуальные цены
    for item in cart:
        product = item['product']
        # Выбираем цену
        price = product.price_pro if is_pro else product.price_retail
        
        # Записываем в объект item (чтобы было доступно в шаблоне)
        item['price'] = price
        item['total_price'] = price * item['quantity']
        
        total_price += item['total_price']
    # -----------------------------------------------------

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем заказ в БД
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            # Важно: сохраняем уже посчитанную сумму
            order.total_cost = total_price 
            order.save()

            # 2. Переносим товары из корзины в OrderItem
            order_items_list = []
            
            for item in cart:
                # Цены уже посчитаны в начале функции (в item['price'])
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                order_items_list.append(order_item)

            # 3. Инициализируем оплату в Т-Банке
            tinkoff = TinkoffPayment()
            
            domain = request.build_absolute_uri('/')[:-1] 
            success_url = domain + reverse('payment_success')
            fail_url = domain + reverse('payment_failed')

            try:
                # Отправляем запрос в банк
                response = tinkoff.init_payment(order, order_items_list, success_url, fail_url)

                if response.get("Success"):
                    cart.clear()
                    order.payment_id = response.get("PaymentId")
                    order.save()
                    return redirect(response.get("PaymentURL"))
                else:
                    # Ошибка логики банка (например, неверный терминал)
                    return render(request, 'orders/error.html', {
                        'message': response.get("Message", "Ошибка банка"), 
                        'details': response.get("Details", "")
                    })
            except Exception as e:
                # Ошибка соединения (интернет, DNS и т.д.)
                return render(request, 'orders/error.html', {
                    'message': "Ошибка соединения с банком",
                    'details': str(e)
                })

    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name, 
                'last_name': request.user.last_name, 
                'email': request.user.email
            }
        form = OrderCreateForm(initial=initial_data)

    # Передаем total_price в контекст
    return render(request, 'orders/create.html', {
        'cart': cart, 
        'form': form,
        'total_price': total_price
    })

# Остальные функции (payment_success, payment_failed, webhook) оставляем без изменений
def payment_success(request):
    return render(request, 'orders/success.html')

def payment_failed(request):
    return render(request, 'orders/failed.html')

@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            # Получаем ID от банка (например "7_1707234567")
            order_id_raw = data.get('OrderId')
            
            # Отделяем реальный ID заказа (цифру 7) от хвоста
            if '_' in str(order_id_raw):
                order_id = order_id_raw.split('_')[0]
            else:
                order_id = order_id_raw
                
            status = data.get('Status')
            
            # Для модели Order нужен импорт
            from .models import Order 
            
            if status == 'CONFIRMED':
                order = get_object_or_404(Order, id=order_id)
                order.paid = True
                order.status = 'paid'
                order.save()
                
            return HttpResponse("OK", content_type="text/plain")
        except Exception as e:
            print(f"Webhook error: {e}") # Для отладки в логах
            return HttpResponse("FAIL", status=400)
    return HttpResponse("OK")