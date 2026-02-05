from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import format_html

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Какие колонки показывать в списке пользователей
    list_display = ('username', 'email', 'full_name', 'status_colored', 'is_staff')
    
    # Фильтры справа (чтобы быстро найти "На проверке")
    list_filter = ('status', 'is_staff', 'is_superuser')
    
    # Поля, по которым можно искать
    search_fields = ('username', 'first_name', 'last_name', 'email')

    # Добавляем наши поля (статус и фото) в форму редактирования
    fieldsets = UserAdmin.fieldsets + (
        ('Статус косметолога', {'fields': ('status', 'license_photo', 'preview_photo')}),
    )
    
    # Делаем поле фото доступным только для чтения в виде картинки (для удобства)
    readonly_fields = ('preview_photo',)

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Имя и Фамилия"

    # Цветной статус для наглядности
    def status_colored(self, obj):
        colors = {
            'client': 'gray',
            'pending': 'orange',
            'approved': 'green',
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"

    # Превью фото диплома прямо в админке
    def preview_photo(self, obj):
        if obj.license_photo:
            return format_html('<a href="{}" target="_blank"><img src="{}" style="max-height: 200px;"/></a>', obj.license_photo.url, obj.license_photo.url)
        return "Нет фото"
    preview_photo.short_description = "Предпросмотр документа"