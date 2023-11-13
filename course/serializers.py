from rest_framework import serializers

from .models import Course, Category


class CategorySerailizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'title',
            'image',
            'cours_count'
        ]


class CourseSerializera(serializers.ModelSerializer):
    category = CategorySerailizer(many=False)

    class Meta:
        model = Course
        fields = [
            'title',
            'price',
            'image',
            'category',
            'degree',
            'rating',
            'section_count',
            'lesson_count',
            'comment_count',
        ]
