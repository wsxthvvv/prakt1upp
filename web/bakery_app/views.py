from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .models import *
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import login, logout
from basket.basket import Basket
from basket.forms import BasketAddProductForm

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
    basket = Basket(request)
    baking_list = []
    for product in Baking.objects.filter(is_exists=True):
        baking_list.append({
            'product': product,
            'quantity': basket.get_quantity('baking', product),
        })
    drink_list = []
    for product in Drink.objects.filter(is_exists=True):
        drink_list.append({
            'product': product,
            'quantity': basket.get_quantity('drink', product),
        })
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

def get_category_products(basket, category):
    baking_list = []
    for product in Baking.objects.filter(category=category, is_exists=True):
        baking_list.append({
            'product': product,
            'quantity': basket.get_quantity('baking', product),
        })
    drink_list = []
    for product in Drink.objects.filter(category=category, is_exists=True):
        drink_list.append({
            'product': product,
            'quantity': basket.get_quantity('drink', product),
        })
    return baking_list, drink_list

@login_required(login_url='/login/')
def my_orders_views(request):
    order_list = Order.objects.filter(user=request.user)
    return render(request, 'order/my_orders.html', {'order_list': order_list})


@method_decorator(permission_required('bakery_app.view_category', login_url='/login/'), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'category_list'

@method_decorator(permission_required('bakery_app.view_category', login_url='/login/'), name='dispatch')
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        basket = Basket(self.request)
        baking_list, drink_list = get_category_products(basket, self.object)
        context['baking_list'] = baking_list
        context['drink_list'] = drink_list
        return context

@method_decorator(permission_required('bakery_app.add_category', login_url='/login/'), name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')

@method_decorator(permission_required('bakery_app.change_category', login_url='/login/'), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category_list')

@method_decorator(permission_required('bakery_app.delete_category', login_url='/login/'), name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

@method_decorator(permission_required('bakery_app.view_baking', login_url='/login/'), name='dispatch')
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
        basket = Basket(self.request)
        context['form_basket'] = BasketAddProductForm()
        context['cart_quantity'] = basket.get_quantity('baking', self.object)
        return context

@method_decorator(permission_required('bakery_app.add_baking', login_url='/login/'), name='dispatch')
class BakingCreateView(CreateView):
    model = Baking
    form_class = BakingForm
    template_name = 'baking/baking_form.html'
    success_url = reverse_lazy('baking_list')

@method_decorator(permission_required('bakery_app.change_baking', login_url='/login/'), name='dispatch')
class BakingUpdateView(UpdateView):
    model = Baking
    form_class = BakingForm
    template_name = 'baking/baking_form.html'
    success_url = reverse_lazy('baking_list')

@method_decorator(permission_required('bakery_app.delete_baking', login_url='/login/'), name='dispatch')
class BakingDeleteView(DeleteView):
    model = Baking
    template_name = 'baking/baking_confirm_delete.html'
    success_url = reverse_lazy('baking_list')

@method_decorator(permission_required('bakery_app.view_drink', login_url='/login/'), name='dispatch')
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
        basket = Basket(self.request)
        context['form_basket'] = BasketAddProductForm()
        context['cart_quantity'] = basket.get_quantity('drink', self.object)
        return context

@method_decorator(permission_required('bakery_app.add_drink', login_url='/login/'), name='dispatch')
class DrinkCreateView(CreateView):
    model = Drink
    form_class = DrinkForm
    template_name = 'drink/drink_form.html'
    success_url = reverse_lazy('drink_list')

@method_decorator(permission_required('bakery_app.change_drink', login_url='/login/'), name='dispatch')
class DrinkUpdateView(UpdateView):
    model = Drink
    form_class = DrinkForm
    template_name = 'drink/drink_form.html'
    success_url = reverse_lazy('drink_list')

@method_decorator(permission_required('bakery_app.delete_drink', login_url='/login/'), name='dispatch')
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

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.author_name = self.request.user.username
        return super().form_valid(form)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    success_url = reverse_lazy('review_list')

    def get_queryset(self):
        if self.request.user.has_perm('bakery_app.change_review'):
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

@method_decorator(login_required(login_url='/login/'), name='dispatch')
class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    success_url = reverse_lazy('review_list')

    def get_queryset(self):
        if self.request.user.has_perm('bakery_app.delete_review'):
            return Review.objects.all()
        return Review.objects.filter(user=self.request.user)

@method_decorator(permission_required('bakery_app.view_order', login_url='/login/'), name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'order_list'

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        if self.request.user.has_perm('bakery_app.view_order'):
            return Order.objects.all()
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user)
        return Order.objects.none()

@method_decorator(permission_required('bakery_app.change_order', login_url='/login/'), name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_edit.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ обновлён!')
        return super().form_valid(form)

@method_decorator(permission_required('bakery_app.delete_order', login_url='/login/'), name='dispatch')
class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/order_confirm_delete.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        messages.success(self.request, 'Заказ удалён!')
        return super().form_valid(form)

@method_decorator(permission_required('bakery_app.view_profile', login_url='/login/'), name='dispatch')
class ProfileListView(ListView):
    model = Profile
    template_name = 'profile/profile_list.html'
    context_object_name = 'profile_list'

@method_decorator(permission_required('bakery_app.view_profile', login_url='/login/'), name='dispatch')
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

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home')
    else:
        form = LoginForm()
    context = {
        'form' : form
    }
    return render(request, 'auth/login.html', context)
    
def registration_user(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home')
    else:
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'auth/registration.html', context)
    
def logout_user(request):
    logout(request)
    return redirect('home')
