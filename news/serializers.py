from rest_framework import serializers

from .models import Tag, New


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class NewSerializer(serializers.ModelSerializer):
    view = serializers.SerializerMethodField()

    def get_view(self, news):
        return news.newsview_set.all().count()

    class Meta:
        model = New
        fields = ['id', 'title', 'image', 'content', 'view', 'tag', 'created_at']
