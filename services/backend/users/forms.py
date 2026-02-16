from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    """Форма регистрации нового клиента"""
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ('username', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.verification_status = 'none' 
        if commit:
            user.save()
        return user

class UpgradeRequestForm(forms.ModelForm):
    """Форма подачи заявки на спец. цены"""
    class Meta:
        model = User
        fields = ('requested_role', 'license_photo')
        widgets = {
            'requested_role': forms.RadioSelect(attrs={'class': 'space-y-2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requested_role'].required = True
        self.fields['license_photo'].required = True
        self.fields['requested_role'].label = "Желаемая специальность"
        
        # --- ЛОГИКА: Убираем роли, которые уже есть у пользователя ---
        if self.instance and self.instance.pk:
            current_choices = list(self.fields['requested_role'].choices)
            new_choices = []
            for role_code, role_label in current_choices:
                # Если роль уже есть - пропускаем её
                if role_code == 'cosmetologist' and self.instance.is_cosmetologist:
                    continue
                if role_code == 'manicurist' and self.instance.is_manicurist:
                    continue
                new_choices.append((role_code, role_label))
            
            self.fields['requested_role'].choices = new_choices