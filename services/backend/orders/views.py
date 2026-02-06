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

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # 1. Сохраняем заказ в БД
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_cost = 0 # Посчитаем ниже
            order.save()

            # 2. Переносим товары из корзины в OrderItem
            total_price = 0
            order_items_list = []
            
            # Определяем цену (PRO или обычная)
            is_pro = request.user.is_authenticated and request.user.status == 'approved'

            for item in cart:
                product = item['product']
                price = product.price_pro if is_pro else product.price_retail
                
                order_item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=price,
                    quantity=item['quantity']
                )
                order_items_list.append(order_item)
                total_price += price * item['quantity']

            # Обновляем общую сумму заказа
            order.total_cost = total_price
            order.save()

            # 3. Инициализируем оплату в Т-Банке
            tinkoff = TinkoffPayment()
            
            # Строим полные URL для возврата (с доменом)
            domain = request.build_absolute_uri('/')[:-1] 
            success_url = domain + reverse('payment_success')
            fail_url = domain + reverse('payment_failed')

            # Отправляем запрос в банк
            response = tinkoff.init_payment(order, order_items_list, success_url, fail_url)

            if response.get("Success"):
                # Если все ок, очищаем корзину и перекидываем на оплату
                cart.clear()
                # Сохраняем ID платежа банка, чтобы потом проверить статус
                order.payment_id = response.get("PaymentId")
                order.save()
                return redirect(response.get("PaymentURL"))
            else:
                # Ошибка со стороны банка
                return render(request, 'orders/error.html', {'message': response.get("Message"), 'details': response.get("Details")})

    else:
        # Автозаполнение формы, если пользователь вошел
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name, 
                'last_name': request.user.last_name, 
                'email': request.user.email
            }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

def payment_success(request):
    return render(request, 'orders/success.html')

def payment_failed(request):
    return render(request, 'orders/failed.html')

# WEBHOOK (Оповещение от банка)
@csrf_exempt
def payment_notification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Тут по-хорошему нужно проверять Token входящего запроса для безопасности!
            
            order_id = data.get('OrderId')
            status = data.get('Status')
            
            if status == 'CONFIRMED':
                order = get_object_or_404(Order, id=order_id)
                order.paid = True
                order.status = 'paid'
                order.save()
                
            return HttpResponse("OK", content_type="text/plain")
        except:
            return HttpResponse("FAIL", status=400)
    return HttpResponse("OK")