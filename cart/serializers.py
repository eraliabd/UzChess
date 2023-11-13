from rest_framework import serializers
from rest_framework.validators import ValidationError

from django.utils.translation import gettext_lazy as _

from .models import CartItem, Order
from course.serializers import CourseSerializera
from library.serializers import BookSerializer
from user.models import CustomUser as User


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'user',
            'book',
            'quantity'
        ]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'book',
            'quantity',
        ]


class CartItemgetSerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = CartItem
        fields = [
            'id',
            'book',
            'quantity',
        ]


class CartItemValuesSerailzier(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title',
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'book',
        ]


class UserCartItemGetSerializer(serializers.ModelSerializer):
    user_cart_item = CartItemgetSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'full_name',
            'phone_number',
            'email',
            'user_cart_item',
        ]


class OrderGetSerializer(serializers.ModelSerializer):
    orders = CartItemValuesSerailzier(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'orders',
            'full_name',
            'phone_number',
            'email',
            'status'
        ]


class OrderCreateSeializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'orders',
            'full_name',
            'phone_number',
            'email',
        ]


class UserOrderSerializer(serializers.ModelSerializer):
    orders = OrderGetSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'orders',
        ]
