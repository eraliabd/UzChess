from django.urls import path, include
from .views import CourseViews, LessonViews, CourseDetailView, ComplaintView

urlpatterns = [
    path('', CourseViews.as_view(), name='cours_main'),
    path('lesson/<int:pk>/', LessonViews.as_view(), name='lesson'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course'),
    path('complaint/', ComplaintView.as_view(), name='complaint'),
]
