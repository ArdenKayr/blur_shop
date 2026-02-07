from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpgradeRequestForm

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

@login_required
def profile(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/profile.html')

@login_required
def upgrade_to_pro(request):
    """Страница подачи заявки на профи"""
    if request.method == 'POST':
        form = UpgradeRequestForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.verification_status = 'pending' 
            user.save()
            return render(request, 'users/upgrade_success.html')
    else:
        form = UpgradeRequestForm(instance=request.user)
    
    return render(request, 'users/upgrade_pro.html', {'form': form})

def about(request):
    """Страница О бренде"""
    return render(request, 'users/about.html')