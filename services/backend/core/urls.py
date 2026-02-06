from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Импортируем views из папки core (там только about)

urlpatterns = [
    # 1. Админка
    path('admin/', admin.site.urls),

    # 2. Приложения (через include)
    path('users/', include('users.urls')),
    path('cart/', include('cart.urls')),      # Корзина
    
    # 3. Страница "О бренде" (она в core/views.py)
    path('about/', views.about, name='about'),

    # 4. Главная страница -> каталог товаров (ВАЖНО: include, а не views.catalog)
    path('', include('products.urls')),

    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)