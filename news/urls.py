from django.urls import path

from .views import TagListAPIView, NewsListAPIView, NewQueryListAPIView, NewsDetailAPIView

urlpatterns = [
    path('tag/', TagListAPIView.as_view(), name='tag'),
    path('', NewsListAPIView.as_view(), name='new'),
    path('<int:pk>/', NewsDetailAPIView.as_view(), name='new-detail'),
    path('search/', NewQueryListAPIView.as_view(), name='new-search'),
]
