from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.response import Response
from .models import Course, Lesson, Complaint
from .serializers import CourseSerializers, LessonSerializers, CommentSerializers, ComplaintSerializer
from rest_framework.pagination import PageNumberPagination

from django_filters import rest_framework as django_filters
from .filter import CourseFilter


class PagePagination(PageNumberPagination):
    page_size = 4


class CourseViews(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers

    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = CourseFilter
    search_fields = ['title']

    pagination_class = PagePagination


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers

    def retrieve(self, request, *args, **kwargs):
        course = self.get_object()
        comments = course.comment.all()
        lessons = course.lesson.all()
        serializer_course = self.get_serializer(course)
        serializer_lesson = LessonSerializers(lessons, many=True)
        serializer_comment = CommentSerializers(comments, many=True)
        response_data = {
            'course': serializer_course.data,
            'lesson': serializer_lesson.data,
            'comment': serializer_comment.data,
        }
        return Response(response_data)


class LessonViews(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializers

    def retrieve(self, request, *args, **kwargs):
        lesson = self.get_object()
        lessons = Lesson.objects.filter(cours=lesson.cours)
        serializer = LessonSerializers(lessons, many=True)
        serializer_id = self.get_serializer(lesson)
        data = {
            'lesson': serializer_id.data,
            'lessons': serializer.data
        }
        return Response(data)


class ComplaintView(generics.CreateAPIView):
    queryset = Complaint.objects.all()
    serializer_class = CommentSerializers
