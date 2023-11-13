from rest_framework import serializers
from .models import Course, Lesson, Comment, Complaint


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (

            'title',
            'price',
            'image',
            'category',
            'degree',
            'rating',
            'section_count',
            'lesson_count',
            'comment_count'
        )


class LessonSerializers(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'cours',
            'title',
            'text',
            'url',
            'image'
        )


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'course',
            'text',
            'rate'
        )


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = (
            'cours',
            'complaint',
            'text'
        )
