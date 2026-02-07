from django.urls import path
from . import views

urlpatterns = [
    # Главная страница (Каталог)
    path('', views.catalog, name='catalog'),
    
    # Страница категории
    path('category/<slug:category_slug>/', views.catalog, name='category_detail'),
    
    # --- ВОТ ЭТОЙ СТРОКИ НЕ ХВАТАЕТ ---
    # Карточка товара
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('favorite/<slug:product_slug>/', views.toggle_favorite, name='toggle_favorite'),
]