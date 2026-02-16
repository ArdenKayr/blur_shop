from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product'] # Чтобы не грузить выпадающий список, если товаров много
    extra = 0 # Убираем пустые строки для новых товаров

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Колонки в общем списке
    list_display = [
        'id', 'first_name', 'last_name', 'phone', 
        'email', 'address', 'paid', 'status', 
        'total_cost', 'created'
    ]
    
    # Фильтры справа (по статусу и оплате)
    list_filter = ['paid', 'status', 'created']
    
    # Поля, которые можно менять прямо из общего списка (удобно для статусов)
    list_editable = ['paid', 'status']
    
    # Поиск по имени, фамилии или email
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    
    # Встраиваем товары внутрь заказа
    inlines = [OrderItemInline]
    
    # Группировка полей при просмотре заказа
    fieldsets = (
        ('Данные клиента', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone', 'address')
        }),
        ('Статус и оплата', {
            'fields': ('status', 'paid', 'total_cost', 'payment_id')
        }),
        ('Даты', {
            'fields': ('created', 'updated')
        }),
    )
    
    # Поля, которые нельзя менять вручную (чтобы не сломать историю)
    readonly_fields = ('created', 'updated', 'payment_id')