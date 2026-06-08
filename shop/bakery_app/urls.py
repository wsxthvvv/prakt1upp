from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_views, name='home'),
    path('about/', about_views, name='about'),
    path('about/contacts/', contacts_views, name='contacts'),
    path('about/location/', location_views, name='location'),
    path('products/categories/', categories_views, name='categories'),
    path('products/', products_views, name='products'),
    path('cart/', cart_views, name='cart'),
    path('delivery/', delivery_views, name='delivery'),
]