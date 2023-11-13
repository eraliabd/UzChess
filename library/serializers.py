from rest_framework import serializers

from .models import BookCategory, Book, Author


class BookCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = BookCategory
        fields = ['id', 'title']


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'full_name']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'content', 'price', 'old_price', 'number_of_pages', 'is_top', 'degree', 'author',
            'category', 'created_at'
        ]


class TopRecommendBookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'image', 'author'
        ]

    def get_author(self, obj):
        author_full_name_split = obj.author.full_name.split()
        # print(parts)
        formatted_full_name = f"{author_full_name_split[0][0]}.{author_full_name_split[-1]}"
        return formatted_full_name
