from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from bakery_app.models import Baking, Drink, OrderItem

from .basket import Basket
from .forms import BasketAddProductForm, OrderForm


def _get_product(product_type, product_id):
    if product_type == 'baking':
        return get_object_or_404(Baking, pk=product_id)
    return get_object_or_404(Drink, pk=product_id)


def basket_detail(request):
    basket = Basket(request)
    return render(request, 'basket/detail.html', {'basket': basket})


@require_POST
def basket_add(request, product_type, product_id):
    basket = Basket(request)
    product = _get_product(product_type, product_id)
    form = BasketAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        basket.add(
            product_type,
            product,
            count=cd['count'],
            update_count=cd['reload'],
        )
    return redirect('basket_detail')


def basket_remove(request, product_type, product_id):
    basket = Basket(request)
    product = _get_product(product_type, product_id)
    basket.remove(product_type, product)
    return redirect('basket_detail')


def basket_clear(request):
    basket = Basket(request)
    basket.clear()
    return redirect('basket_detail')


@login_required(login_url='/login/')
def open_order(request):
    form_order = OrderForm()
    return render(request, 'order/order_form.html', {'form_order': form_order})


@login_required(login_url='/login/')
def basket_buy(request):
    basket = Basket(request)
    if len(basket) == 0:
        return redirect('products')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.price = basket.get_total_price()
            order.customer_name = f'{order.buyer_firstname} {order.buyer_name}'.strip()
            order.address = order.delivery_address
            order.status = 'новый'
            order.save()
            for item in basket:
                OrderItem.objects.create(
                    order=order,
                    baking=item['product'] if item['product_type'] == 'baking' else None,
                    drink=item['product'] if item['product_type'] == 'drink' else None,
                    quantity=item['count'],
                )
            basket.clear()
            return redirect('basket_detail')

    return redirect('order_open')
