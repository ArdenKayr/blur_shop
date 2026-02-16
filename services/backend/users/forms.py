from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import ProApplication

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UpgradeRequestForm(forms.ModelForm):
    class Meta:
        model = ProApplication
        fields = ('role', 'license_photo')
        widgets = {
            'role': forms.RadioSelect(attrs={'class': 'space-y-2'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        # Принимаем user в конструктор, чтобы фильтровать варианты
        super().__init__(*args, **kwargs)
        self.user = user
        
        self.fields['role'].required = True
        self.fields['license_photo'].required = True
        self.fields['role'].label = "Выберите специализацию"
        self.fields['license_photo'].label = "Загрузите диплом"

        # Фильтруем список ролей
        current_choices = list(self.fields['role'].choices)
        available_choices = []
        
        # Получаем список ролей, на которые УЖЕ подана заявка (и она висит)
        pending_roles = ProApplication.objects.filter(
            user=user, 
            status='pending'
        ).values_list('role', flat=True)

        for code, label in current_choices:
            # 1. Если роль уже получена (есть доступ) - скрываем
            if code == 'cosmetologist' and user.is_cosmetologist:
                continue
            if code == 'manicurist' and user.is_manicurist:
                continue
            
            # 2. Если заявка на эту роль уже висит - скрываем
            if code in pending_roles:
                continue
                
            available_choices.append((code, label))
        
        self.fields['role'].choices = available_choices

    def clean(self):
        cleaned_data = super().clean()
        if not self.fields['role'].choices:
            raise forms.ValidationError("Нет доступных ролей для подачи заявки.")
        return cleaned_data