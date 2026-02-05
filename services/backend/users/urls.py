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
    
    # --- НОВЫЙ МАРШРУТ: ЛИЧНЫЙ КАБИНЕТ ---
    path('profile/', views.profile, name='profile'),
    
    # Стать партнером
    path('upgrade/pro/', views.upgrade_to_pro, name='upgrade_pro'),

    # --- СБРОС ПАРОЛЯ ---
    
    # # 1. Страница ввода Email
    # path('password_reset/', auth_views.PasswordResetView.as_view(
    #     template_name='users/password_reset_form.html',
    #     email_template_name='users/password_reset_email.html', # Текст письма (стандартный)
    #     success_url='/users/password_reset/done/'
    # ), name='password_reset'),

    # # 2. Сообщение "Письмо отправлено"
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
    #     template_name='users/password_reset_done.html'
    # ), name='password_reset_done'),

    # # 3. Ссылка из письма (ввод нового пароля)
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    #     template_name='users/password_reset_confirm.html',
    #     success_url='/users/reset/done/'
    # ), name='password_reset_confirm'),

    # # 4. Сообщение "Пароль успешно изменен"
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
    #     template_name='users/password_reset_complete.html'
    # ), name='password_reset_complete'),
]