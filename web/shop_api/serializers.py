from rest_framework import serializers

from bakery_app.models import *

class BakingSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(label="Цена", max_digits=10, decimal_places=2)

    class Meta:

        model = Baking
        fields = [
            'name',
            'description',
            'price',
            'category',
        ]

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
        ]

class DrinkSerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(label="Цена", max_digits=10, decimal_places=2)

    class Meta:

        model = Drink
        fields = [
            'name',
            'description',
            'price',
            'category',
        ]

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'user',
            'phone',
            'address',
        ]

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = [
            'author_name',
            'text',
            'rating',
        ]

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'buyer_firstname',
            'buyer_name',
            'buyer_surname',
            'comment',
            'delivery_address',
            'delivery_type',
            'phone',
            'status',
            'price',
        ]

class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            'order',
            'baking',
            'drink',
            'quantity',
        ]

class DeliverySerializer(serializers.ModelSerializer):

    price = serializers.DecimalField(label="Цена", max_digits=10, decimal_places=2)

    class Meta:
        model = Delivery
        fields = [
            'name',
            'description',
            'price',
        ]

class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = [
            'name',
            'description',
            'discount',
        ]

