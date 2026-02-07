from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Приватное хранилище для документов
protected_storage = FileSystemStorage(
    location=os.path.join(settings.BASE_DIR, 'protected_media'),
    base_url='/protected_media/'
)

class User(AbstractUser):
    # Статус рассмотрения заявки
    APPLICATION_STATUS = (
        ('none', 'Нет заявки'),
        ('pending', 'На проверке'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    )
    
    # Роли, которые выбирает пользователь
    ROLE_CHOICES = (
        ('cosmetologist', 'Косметолог'),
        ('manicurist', 'Мастер маникюра/педикюра'),
    )

    # Поле статуса заявки
    verification_status = models.CharField(
        max_length=20, 
        choices=APPLICATION_STATUS, 
        default='none',
        verbose_name="Статус заявки"
    )
    
    # Какую роль запросил пользователь (для админки)
    requested_role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Запрошенная роль"
    )
    
    # Реальные права доступа (галочки)
    is_cosmetologist = models.BooleanField("Является косметологом", default=False)
    is_manicurist = models.BooleanField("Является мастером маникюра", default=False)
    
    license_photo = models.ImageField(
        upload_to='cosmetologist_docs/', 
        storage=protected_storage,
        null=True, 
        blank=True,
        verbose_name="Документ об образовании"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"