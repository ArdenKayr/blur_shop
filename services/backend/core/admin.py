from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price_list_link')
    
    def price_list_link(self, obj):
        if obj.price_list:
            return "Файл загружен"
        return "Нет файла"
    price_list_link.short_description = "Прайс-лист"