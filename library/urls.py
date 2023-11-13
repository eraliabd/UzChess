from django.urls import path

from .views import BookListCreateView, AuthorListCreateView, BookCategoryListCreateView, TopBookListView, \
    RecommendBookListView, BookDetailView, BookQueryListView

urlpatterns = [
    path('book/', BookListCreateView.as_view(), name='book'),
    path('book/search/', BookQueryListView.as_view(), name='book-query'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('top-book/', TopBookListView.as_view(), name='top_book'),
    path('recommend-book/', RecommendBookListView.as_view(), name='recommend_book'),

    path('category/', BookCategoryListCreateView.as_view(), name='category'),
    path('author/', AuthorListCreateView.as_view(), name='author'),
]
