from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser

from django.db.models import Q

from .models import New, Tag, NewsView
from .serializers import NewSerializer, TagSerializer


class TagListAPIView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class NewsListAPIView(ListCreateAPIView):
    queryset = New.objects.all().order_by('-created_at')
    serializer_class = NewSerializer
    parser_classes = [FormParser, MultiPartParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


class NewsDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        device_id = self.request.META.get("HTTP_USER_AGENT", "")
        # print("Device ID: ", device_id)

        if request.user.is_authenticated:
            if device_id is not None:
                NewsView.objects.update_or_create(news=instance, user=request.user, device_id=device_id)

            NewsView.objects.update_or_create(news=instance, user=request.user)

        elif device_id is not None:
            NewsView.objects.update_or_create(news=instance, device_id=device_id)

        return Response(serializer.data)


class NewQueryListAPIView(ListAPIView):
    serializer_class = NewSerializer

    def get_queryset(self):
        search_query = self.request.query_params.get('search')

        if search_query:
            return New.objects.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            ).order_by('-created_at')

        return {"message": "Hech qanday ma’lumot topilmadi!"}
