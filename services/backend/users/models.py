from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

protected_storage = FileSystemStorage(
    location=os.path.join(settings.BASE_DIR, 'protected_media'),
    base_url='/protected_media/'
)

class User(AbstractUser):
    # Статусы для UI (кнопка в шапке)
    APPLICATION_STATUS = (
        ('none', 'Нет активной заявки'),
        ('pending', 'На проверке'),
    )
    
    # Флаг: есть ли хоть одна заявка на проверке?
    verification_status = models.CharField(
        max_length=20, 
        choices=APPLICATION_STATUS, 
        default='none',
        verbose_name="Статус проверки"
    )
    
    # Права доступа (остаются на пользователе)
    is_cosmetologist = models.BooleanField("Доступ: Косметолог", default=False)
    is_manicurist = models.BooleanField("Доступ: Маникюр", default=False)
    
    # Поля requested_role и license_photo убраны отсюда, 
    # так как теперь они живут в отдельных заявках (ProApplication)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class ProApplication(models.Model):
    """Отдельная модель для заявки на специалиста"""
    ROLE_CHOICES = (
        ('cosmetologist', 'Косметолог'),
        ('manicurist', 'Мастер маникюра/педикюра'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name="Пользователь")
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES)
    
    license_photo = models.ImageField(
        upload_to='cosmetologist_docs/', 
        storage=protected_storage,
        verbose_name="Документ"
    )
    
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField("Дата подачи", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на профи"
        verbose_name_plural = "Заявки на профи"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"