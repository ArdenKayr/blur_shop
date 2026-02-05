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
    STATUS_CHOICES = (
        ('client', 'Обычный клиент'),
        ('pending', 'Косметолог (на проверке)'),
        ('approved', 'Косметолог (одобрен)'),
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='client',
        verbose_name="Статус"
    )
    
    license_photo = models.ImageField(
        upload_to='cosmetologist_docs/', 
        storage=protected_storage,
        null=True, 
        blank=True,
        verbose_name="Документ"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"