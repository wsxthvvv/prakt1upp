from django import forms
from .models import *

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
        fields = ['author_name', 'text', 'rating', 'baking', 'drink']

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
        fields = ['customer_name', 'phone', 'address', 'delivery', 'status']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['baking', 'drink', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        baking = cleaned_data.get('baking')
        drink = cleaned_data.get('drink')
        if baking and drink:
            raise forms.ValidationError('Выберите выпечку или напиток, не оба сразу.')
        if not baking and not drink:
            raise forms.ValidationError('Выберите выпечку или напиток.')
        return cleaned_data

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(max_length=MAX_LENGTH, label='Имя клиента')
    phone = forms.CharField(max_length=20, label='Телефон')
    address = forms.CharField(widget=forms.Textarea, label='Адрес доставки')
    delivery = forms.ModelChoiceField(queryset=Delivery.objects.all(), label='Зона доставки')
