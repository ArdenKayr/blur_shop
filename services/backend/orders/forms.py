from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-lg p-3'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-lg p-3'}),
            'email': forms.EmailInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-lg p-3'}),
            'phone': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-lg p-3'}),
            'address': forms.TextInput(attrs={'class': 'w-full bg-gray-50 border border-gray-200 rounded-lg p-3'}),
        }