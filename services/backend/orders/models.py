from django.db import models
from django.conf import settings

class Order(models.Model):
    # Обновленные статусы по вашему ТЗ
    STATUS_CHOICES = (
        ('not_processed', 'Заказ не обработан'),
        ('confirmed', 'Заказ подтвержден'),
        ('shipped', 'Заказ отправлен'),
        ('received', 'Заказ получен'),
        ('canceled', 'Отменен'),
    )

    # Информация о клиенте
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес доставки", max_length=250)
    
    # Данные заказа
    created = models.DateTimeField("Создан", auto_now_add=True)
    updated = models.DateTimeField("Обновлен", auto_now=True)
    paid = models.BooleanField("Оплачено", default=False)
    
    # По умолчанию заказ "Не обработан"
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='not_processed')
    
    # Связь с Т-Банком
    payment_id = models.CharField("ID платежа", max_length=100, blank=True)
    total_cost = models.DecimalField("Сумма", max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', related_name='order_items', on_delete=models.CASCADE, verbose_name="Товар")
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity