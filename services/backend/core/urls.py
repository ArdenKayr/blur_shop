from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Импортируем views из текущей папки (core)

urlpatterns = [
    # 1. Админка
    path('admin/', admin.site.urls),

    # 2. Пользователи (вход, регистрация, профиль)
    path('users/', include('users.urls')),

    # 3. Страница "О бренде" (наша новая)
    path('about/', views.about, name='about'),

    # 4. Товары (Каталог) - ВАЖНО: ставить последним, так как там пустой путь ''
    path('', include('products.urls')),
]

# Раздача медиа-файлов (картинок) в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)