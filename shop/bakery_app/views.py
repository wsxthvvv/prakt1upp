from django.shortcuts import render

def home_views(request):
    return render(request, 'home.html')

def about_views(request):
    return render(request, 'about.html')

def contacts_views(request):
    return render(request, 'contacts.html')

def location_views(request):
    return render(request, 'location.html')

def categories_views(request):
    return render(request, 'categories.html')

def products_views(request):
    return render(request, 'products.html')

def cart_views(request):
    return render(request, 'cart.html')

def delivery_views(request):
    return render(request, 'delivery.html')
