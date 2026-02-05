from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required # Импортируем декоратор
from .forms import RegisterForm

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('catalog')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

# --- НОВАЯ ФУНКЦИЯ ---
@login_required
def profile(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/profile.html')

def upgrade_to_pro(request):
    return render(request, 'users/upgrade_pro.html')