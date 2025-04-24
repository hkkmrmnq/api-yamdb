from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer
)
from reviews.models import Category, Genre, Title, Review


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ViewSet):
    """
    ViewSet для работы с произведениями
    """
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = TitleSerializer

    def retrieve(self, request, pk=None):
        try:
            title = Title.objects.get(id=pk)
            serializer = self.serializer_class(title)
            return Response(serializer.data)
        except Title.DoesNotExist:
            return Response(status=404)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        try:
            title = Title.objects.get(id=pk)
            serializer = self.serializer_class(title, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except Title.DoesNotExist:
            return Response(status=404)

    def destroy(self, request, pk=None):
        try:
            title = Title.objects.get(id=pk)
            title.delete()
            return Response(status=204)
        except Title.DoesNotExist:
            return Response(status=404)


class ReviewViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции CRUD для модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Обрабатывает операции CRUD для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_review(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=title)

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(
            author=self.request.user,
            review=review
        )
