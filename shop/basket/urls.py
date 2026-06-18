from django.urls import path

from .views import (
    basket_add,
    basket_buy,
    basket_clear,
    basket_detail,
    basket_remove,
    open_order,
)

urlpatterns = [
    path('', basket_detail, name='basket_detail'),
    path('add/<str:product_type>/<int:product_id>/', basket_add, name='basket_add'),
    path('remove/<str:product_type>/<int:product_id>/', basket_remove, name='basket_remove'),
    path('clear/', basket_clear, name='basket_clear'),
    path('buy/', basket_buy, name='basket_buy'),
    path('create_order/', open_order, name='order_open'),
]
