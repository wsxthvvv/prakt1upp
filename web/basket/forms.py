from django import forms

from bakery_app.models import Order


class BasketAddProductForm(forms.Form):
    count = forms.IntegerField(
        label='Количество',
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
    reload = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput(),
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'buyer_firstname',
            'buyer_name',
            'buyer_surname',
            'comment',
            'delivery_address',
            'delivery_type',
        )
