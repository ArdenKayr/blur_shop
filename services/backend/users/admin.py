from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProApplication
from django.utils.html import format_html
from django.contrib import messages

# Админка пользователей (стандартная + флаги прав)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'roles_display', 'verification_status', 'is_staff')
    list_filter = ('is_cosmetologist', 'is_manicurist')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Права специалиста', {
            'fields': ('is_cosmetologist', 'is_manicurist')
        }),
        ('Статус', {
            'fields': ('verification_status',)
        }),
    )

    def roles_display(self, obj):
        roles = []
        if obj.is_cosmetologist: roles.append("Косметолог")
        if obj.is_manicurist: roles.append("Маникюр")
        return ", ".join(roles) if roles else "Клиент"
    roles_display.short_description = "Права"


# Админка ЗАЯВОК (новая)
@admin.register(ProApplication)
class ProApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'role_display', 'preview_photo', 'status_colored', 'created_at')
    list_filter = ('status', 'role')
    actions = ['approve_application', 'reject_application']
    
    # Показываем сначала новые
    ordering = ['status', '-created_at']

    def role_display(self, obj):
        return obj.get_role_display()
    role_display.short_description = "Специализация"

    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = "Статус"

    def preview_photo(self, obj):
        if obj.license_photo:
            return format_html(
                '<a href="{}" target="_blank" style="background: #E08D79; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none;">📄 Открыть диплом</a>', 
                obj.license_photo.url
            )
        return "-"
    preview_photo.short_description = "Документ"

    # --- ДЕЙСТВИЯ ---

    @admin.action(description="✅ ОДОБРИТЬ выбранные заявки")
    def approve_application(self, request, queryset):
        count = 0
        for app in queryset.filter(status='pending'):
            user = app.user
            
            # Выдаем права
            if app.role == 'cosmetologist':
                user.is_cosmetologist = True
            elif app.role == 'manicurist':
                user.is_manicurist = True
            
            # Если больше нет висящих заявок, снимаем статус "На проверке" с юзера
            other_pending = user.applications.filter(status='pending').exclude(id=app.id).exists()
            if not other_pending:
                user.verification_status = 'none'
            
            user.save()
            
            # Закрываем заявку
            app.status = 'approved'
            app.save()
            count += 1
            
        self.message_user(request, f"Одобрено заявок: {count}")

    @admin.action(description="❌ ОТКЛОНИТЬ выбранные заявки")
    def reject_application(self, request, queryset):
        for app in queryset.filter(status='pending'):
            app.status = 'rejected'
            app.save()
            
            # Обновляем статус юзера, если у него больше нет заявок
            user = app.user
            other_pending = user.applications.filter(status='pending').exclude(id=app.id).exists()
            if not other_pending:
                user.verification_status = 'none'
            user.save()
            
        self.message_user(request, "Заявки отклонены.", level=messages.WARNING)