from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

class BakingForm(forms.ModelForm):
    class Meta:
        model = Baking
        fields = ['name', 'description', 'price', 'weight', 'diameter', 'filling', 'photo', 'is_exists', 'category']

class DrinkForm(forms.ModelForm):
    class Meta:
        model = Drink
        fields = ['name', 'description', 'price', 'volume', 'photo', 'is_exists', 'category']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'baking', 'drink']

    def clean(self):
        cleaned_data = super().clean()
        baking = cleaned_data.get('baking')
        drink = cleaned_data.get('drink')
        if baking and drink:
            raise forms.ValidationError('Выберите выпечку или напиток, не оба сразу.')
        if not baking and not drink:
            raise forms.ValidationError('Выберите выпечку или напиток.')
        return cleaned_data

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'buyer_firstname', 'buyer_name', 'buyer_surname',
            'comment', 'delivery_address', 'delivery_type',
            'phone', 'status',
        ]

class RegistrationForm( UserCreationForm):
    username = forms.CharField(
        label='Логин пользователя',
        widget=forms. TextInput(attrs={'class':'form-control',}),
        min_length=2
    )
    email = forms.CharField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class':'form-control',}),
    )
    password1 = forms.CharField(
        label= 'Придумайте пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control',}),
    )

    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control',}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms. CharField(
        label='Логин пользователя',
        widget=forms. TextInput(attrs={'class':'form-control',}),
        min_length=2
    )
    password = forms. CharField(
        label='Введите пароль',
        widget=forms.PasswordInput(attrs={'class':'form-control',}),
    )