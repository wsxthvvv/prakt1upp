from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import *

def home_views(request):
    return render(request, 'home.html')

def about_views(request):
    review_list = Review.objects.all()
    return render(request, 'about.html', {'review_list': review_list})

def contacts_views(request):
    return render(request, 'contacts.html')

def location_views(request):
    return render(request, 'location.html')

def products_views(request):
    cart = request.session.get('cart', {})
    baking_list = []
    for product in Baking.objects.filter(is_exists=True):
        key = f'baking_{product.pk}'
        baking_list.append({'product': product, 'quantity': cart.get(key, 0)})
    drink_list = []
    for product in Drink.objects.filter(is_exists=True):
        key = f'drink_{product.pk}'
        drink_list.append({'product': product, 'quantity': cart.get(key, 0)})
    return render(request, 'products.html', {
        'baking_list': baking_list,
        'drink_list': drink_list,
    })

def delivery_views(request):
    delivery_list = Delivery.objects.all()
    promotion_list = Promotion.objects.filter(is_active=True)
    return render(request, 'delivery.html', {
        'delivery_list': delivery_list,
        'promotion_list': promotion_list,
    })

def get_category_products(cart, category):
    baking_list = []
    for product in Baking.objects.filter(category=category, is_exists=True):
        key = f'baking_{product.pk}'
        baking_list.append({'product': product, 'quantity': cart.get(key, 0)})
    drink_list = []
    for product in Drink.objects.filter(category=category, is_exists=True):
        key = f'drink_{product.pk}'
        drink_list.append({'product': product, 'quantity': cart.get(key, 0)})
    return baking_list, drink_list

def cart_redirect(request, product_type, pk):
    next_page = request.GET.get('next')
    if next_page == 'cart':
        return redirect('cart')
    if next_page == 'category':
        category_id = request.GET.get('category')
        if category_id:
            return redirect('category_detail', pk=category_id)
    if next_page == 'detail':
        if product_type == 'baking':
            return redirect('baking_detail', pk=pk)
        return redirect('drink_detail', pk=pk)
    return redirect(reverse('products') + f'#product-{product_type}-{pk}')

def get_cart_data(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for key, quantity in cart.items():
        product_type, pk = key.split('_')
        if product_type == 'baking':
            product = Baking.objects.filter(pk=pk).first()
        else:
            product = Drink.objects.filter(pk=pk).first()
        if product:
            item_sum = product.price * quantity
            items.append({
                'product': product,
                'type': product_type,
                'quantity': quantity,
                'sum': item_sum,
            })
            total += item_sum
    return items, total

def cart_views(request):
    items, total = get_cart_data(request)
    return render(request, 'cart.html', {'items': items, 'total': total})

def cart_add_views(request, product_type, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        key = f'{product_type}_{pk}'
        cart[key] = cart.get(key, 0) + 1
        request.session['cart'] = cart
    return cart_redirect(request, product_type, pk)

def cart_remove_views(request, product_type, pk):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        key = f'{product_type}_{pk}'
        if key in cart:
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]
        request.session['cart'] = cart
    return cart_redirect(request, product_type, pk)

def cart_checkout_views(request):
    items, total = get_cart_data(request)
    if not items:
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                delivery=form.cleaned_data['delivery'],
                status='новый',
            )
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    baking=item['product'] if item['type'] == 'baking' else None,
                    drink=item['product'] if item['type'] == 'drink' else None,
                    quantity=item['quantity'],
                )
            request.session['cart'] = {}
            messages.success(request, 'Заказ оформлен!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = CheckoutForm()
    return render(request, 'cart_checkout.html', {
        'form': form,
        'items': items,
        'total': total,
    })

def order_create_views(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        item_form = OrderItemForm(request.POST)
        if order_form.is_valid() and item_form.is_valid():
            order = order_form.save()
            item = item_form.save(commit=False)
            item.order = order
            item.save()
            messages.success(request, 'Заказ добавлен!')
            return redirect('order_list')
    else:
        order_form = OrderForm()
        item_form = OrderItemForm()
    return render(request, 'order/order_form.html', {
        'order_form': order_form,
        'item_form': item_form,
    })

class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'category_list'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        baking_list, drink_list = get_category_products(cart, self.object)
        context['baking_list'] = baking_list
        context['drink_list'] = drink_list
        return context

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

class BakingListView(ListView):
    model = Baking
    template_name = 'baking/baking_list.html'
    context_object_name = 'baking_list'

class BakingDetailView(DetailView):
    model = Baking
    template_name = 'baking/baking_detail.html'
    context_object_name = 'baking'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        context['cart_quantity'] = cart.get(f'baking_{self.object.pk}', 0)
        return context

class BakingCreateView(CreateView):
    model = Baking
    form_class = BakingForm
    template_name = 'baking/baking_form.html'
    success_url = reverse_lazy('baking_list')

class BakingUpdateView(UpdateView):
    model = Baking
    form_class = BakingForm
    template_name = 'baking/baking_form.html'
    success_url = reverse_lazy('baking_list')

class BakingDeleteView(DeleteView):
    model = Baking
    template_name = 'baking/baking_confirm_delete.html'
    success_url = reverse_lazy('baking_list')

class DrinkListView(ListView):
    model = Drink
    template_name = 'drink/drink_list.html'
    context_object_name = 'drink_list'

class DrinkDetailView(DetailView):
    model = Drink
    template_name = 'drink/drink_detail.html'
    context_object_name = 'drink'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        context['cart_quantity'] = cart.get(f'drink_{self.object.pk}', 0)
        return context

class DrinkCreateView(CreateView):
    model = Drink
    form_class = DrinkForm
    template_name = 'drink/drink_form.html'
    success_url = reverse_lazy('drink_list')

class DrinkUpdateView(UpdateView):
    model = Drink
    form_class = DrinkForm
    template_name = 'drink/drink_form.html'
    success_url = reverse_lazy('drink_list')

class DrinkDeleteView(DeleteView):
    model = Drink
    template_name = 'drink/drink_confirm_delete.html'
    success_url = reverse_lazy('drink_list')

class ReviewListView(ListView):
    model = Review
    template_name = 'review/review_list.html'
    context_object_name = 'review_list'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'order_list'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ обновлён!')
        return super().form_valid(form)

class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ удалён!')
        return super().form_valid(form)

class ProfileListView(ListView):
    model = Profile
    template_name = 'profile/profile_list.html'
    context_object_name = 'profile_list'

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'

class PromotionListView(ListView):
    model = Promotion
    template_name = 'promotion/promotion_list.html'
    context_object_name = 'promotion_list'

    def get_queryset(self):
        return Promotion.objects.filter(is_active=True)

class PromotionDetailView(DetailView):
    model = Promotion
    template_name = 'promotion/promotion_detail.html'
    context_object_name = 'promotion'
