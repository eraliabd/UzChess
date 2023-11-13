from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import models
from django.utils.translation import gettext_lazy as _

from .serializers import CartItemCreateSerializer, UserCartItemGetSerializer, CartItemUpdateSerializer, OrderCreateSeializer, UserOrderSerializer
from .models import CartItem, Order
from user.models import CustomUser as User

# Create your views here.


class CreateCartItemView(generics.GenericAPIView):
    # queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer

    def post(self, request):
        serailizer = self.get_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)

        user = serailizer.validated_data['user']
        book = serailizer.validated_data['book']
        quantity = serailizer.validated_data['quantity']

        cart_items = CartItem.objects.filter(
            user=user, book=book, is_ordered=False
        )

        if not cart_items.exists():
            cart_items.create(
                user=user,
                book=book,
                quantity=quantity,
                is_ordered=False
            )
            return Response(serailizer.data)
        return Response(
            {
                'message': _("Already Added")
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemUpdateSerializer


class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemCreateSerializer


class CartItemListView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserCartItemGetSerializer


class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderCreateSeializer
    queryset = Order.objects.all()


class UserOrderListView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserOrderSerializer
