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

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}

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
    # Теперь видны все 3 цены
    list_display = ('name', 'category', 'price_retail', 'price_cosmetology', 'price_manicure')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    filter_horizontal = ('filters',) 
    actions = [duplicate_product]