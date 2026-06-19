from .serializers import *
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from bakery_app.models import *
from .permission import *


class BakingViewSet(viewsets.ModelViewSet):
    queryset = Baking.objects.all()
    serializer_class = BakingSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class DrinkViewSet(viewsets.ModelViewSet):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['phone', 'address']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['author_name', 'text']

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['customer_name', 'phone', 'address', 'status']

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['quantity']

class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [CustomPermissions]
    pagination_class = PaginationPage
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
