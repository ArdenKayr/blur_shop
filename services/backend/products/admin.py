from django.contrib import admin
from .models import Product, FilterGroup, FilterValue, CarouselItem # <--- Добавили CarouselItem

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'order', 'is_active')
    list_editable = ('order', 'is_active')

# ... остальной код (FilterGroupAdmin, FilterValueAdmin, ProductAdmin) оставляем как был
@admin.register(FilterGroup)
class FilterGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(FilterValue)
class FilterValueAdmin(admin.ModelAdmin):
    list_display = ('group', 'value')
    list_filter = ('group',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_retail', 'price_pro', 'stock')
    filter_horizontal = ('filters',)