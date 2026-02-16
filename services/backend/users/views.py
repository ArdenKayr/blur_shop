from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpgradeRequestForm
from .models import ProApplication

def register(request):
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
    return render(request, 'users/profile.html')

@login_required
def upgrade_to_pro(request):
    # Если у пользователя уже есть ВСЕ права, редиректим
    if request.user.is_cosmetologist and request.user.is_manicurist:
        return redirect('profile')

    if request.method == 'POST':
        # Передаем user в форму
        form = UpgradeRequestForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            
            # Обновляем статус пользователя (для UI)
            request.user.verification_status = 'pending'
            request.user.save()
            
            return render(request, 'users/upgrade_success.html')
    else:
        form = UpgradeRequestForm(request.user)
    
    # Если вариантов нет (например, на все роли уже подал), говорим об этом
    if not form.fields['role'].choices:
        return render(request, 'users/upgrade_pro.html', {
            'form': form, 
            'no_choices': True
        })
    
    return render(request, 'users/upgrade_pro.html', {'form': form})

def about(request):
    return render(request, 'users/about.html')