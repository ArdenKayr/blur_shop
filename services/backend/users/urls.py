from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Вход
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Выход
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Регистрация
    path('register/', views.register, name='register'),
    
    # Личный кабинет
    path('profile/', views.profile, name='profile'),
    
    # Стать партнером
    path('upgrade/pro/', views.upgrade_to_pro, name='upgrade_pro'),
    
    # О бренде (ЭТОГО НЕ ХВАТАЛО)
    path('about/', views.about, name='about'),
]