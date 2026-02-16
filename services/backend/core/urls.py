from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
]

# Настройка раздачи файлов при разработке
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Исправляем путь для просмотра защищенных файлов в админке
    # Файлы физически лежат в BASE_DIR/protected_media/
    # Ссылка в браузере будет /protected_media/имя_файла
    urlpatterns += static('/protected_media/', document_root=os.path.join(settings.BASE_DIR, 'protected_media'))