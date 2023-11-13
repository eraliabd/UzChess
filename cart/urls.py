from django.urls import path

from .views import CreateCartItemView, CartItemListView, CartItemUpdateView, CartItemDeleteView, OrderCreateView, UserOrderListView

urlpatterns = [
    path('<int:pk>/update/', CartItemUpdateView.as_view()),
    path('<int:pk>/delete/', CartItemDeleteView.as_view()),
    path('add/', CreateCartItemView.as_view()),
    path('user/<int:pk>/', CartItemListView.as_view()),
]

urlpatterns += [
    path('user/order/<int:pk>/', UserOrderListView.as_view()),
    path('order/add/', OrderCreateView.as_view()),
]
