from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.utils.html import format_html

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'verification_status_colored', 'roles_display', 'is_staff')
    list_filter = ('verification_status', 'is_cosmetologist', 'is_manicurist')
    search_fields = ('username', 'first_name', 'last_name', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Статус специалиста', {
            'fields': (
                'verification_status', 
                'requested_role', 
                'license_photo', 
                'preview_photo',
                'is_cosmetologist', 
                'is_manicurist'
            )
        }),
    )
    
    readonly_fields = ('preview_photo', 'requested_role')

    def roles_display(self, obj):
        roles = []
        if obj.is_cosmetologist: roles.append("Косметолог")
        if obj.is_manicurist: roles.append("Маникюр")
        return ", ".join(roles) if roles else "-"
    roles_display.short_description = "Активные роли"

    def verification_status_colored(self, obj):
        colors = {
            'none': 'gray',
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.verification_status, 'black'),
            obj.get_verification_status_display()
        )
    verification_status_colored.short_description = "Заявка"

    def preview_photo(self, obj):
        if obj.license_photo:
            # Ссылка теперь точно ведет на правильный URL
            return format_html(
                '<a href="{}" target="_blank" style="color: #E08D79; font-weight: bold;">'
                '<img src="{}" style="max-height: 150px; border: 1px solid #ddd; padding: 4px; border-radius: 4px; display: block; margin-bottom: 5px;"/>'
                'Открыть оригинал'
                '</a>', 
                obj.license_photo.url, 
                obj.license_photo.url
            )
        return "Нет документа"
    preview_photo.short_description = "Документ"