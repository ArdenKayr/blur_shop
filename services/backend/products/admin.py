from django.contrib import admin
from .models import Product, FilterGroup, FilterValue, CarouselItem, Category

@admin.action(description="Сделать копию")
def duplicate_product(modeladmin, request, queryset):
    for product in queryset:
        old_filters = list(product.filters.all()) if hasattr(product, 'filters') else []
        product.pk = None
        product.id = None
        if hasattr(product, 'name'):
            product.name = f"{product.name} (Копия)"
        product.save()
        if hasattr(product, 'filters'):
            product.filters.set(old_filters)

# --- НОВАЯ МОДЕЛЬ КАТЕГОРИЙ ---
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}

# Остальное без изменений
@admin.register(FilterGroup)
class FilterGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(FilterValue)
class FilterValueAdmin(admin.ModelAdmin):
    list_display = ('value', 'group')
    list_filter = ('group',)

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Добавили category в список
    list_display = ('name', 'category', 'price_retail', 'price_pro')
    list_filter = ('category',) # Фильтр справа по категориям
    search_fields = ('name', 'description')
    filter_horizontal = ('filters',) 
    actions = [duplicate_product]