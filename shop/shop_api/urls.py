from .views import *
from rest_framework import routers

urlpatterns = [
    
]

router = routers.SimpleRouter()
router.register('baking', BakingViewSet, basename='baking')
router.register('category', CategoryViewSet, basename='category')
router.register('drink', DrinkViewSet, basename='drink')
router.register('profile', ProfileViewSet, basename='profile')
router.register('review', ReviewViewSet, basename='review')
router.register('order', OrderViewSet, basename='order')
router.register('orderitem', OrderItemViewSet, basename='orderitem')
router.register('delivery', DeliveryViewSet, basename='delivery')
router.register('promotion', PromotionViewSet, basename='promotion')
urlpatterns += router.urls
