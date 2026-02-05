from django.db import models

class SiteSettings(models.Model):
    """Настройки сайта: прайс-лист, контакты и т.д."""
    price_list = models.FileField(
        upload_to='documents/', 
        verbose_name="Файл прайс-листа",
        help_text="Загрузите PDF или Excel файл. Он будет скачиваться по кнопке 'Прайс-лист'."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return f"Настройки от {self.created_at.strftime('%d.%m.%Y')}"