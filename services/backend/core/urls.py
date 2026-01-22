from django.contrib import admin
from django.urls import path, include  # Не забудь добавить include!
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),  # Подключаем маршруты товаров к корню сайта
]

# Это нужно, чтобы Django умел показывать картинки (uploaded media)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)