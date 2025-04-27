import django_filters
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .permissions import AdminLevelOrReadOnly, OwnerOrModeratorLevelOrReadOnly
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerReadOnly,
    TitleSerializerWrite,
)
from reviews.models import Category, Genre, Review, Title


class CategoryGenreBaseViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """Базовый Вьюсет для работы с категориями и жанрами"""

    permission_classes = (AdminLevelOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')


class CategoryViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreBaseViewSet):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleFilter(django_filters.FilterSet):
    """Filterset для возможности фильтрации произведений по идентификатору."""

    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='exact'
    )
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')


class TitleViewSet(ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = (
        Title.objects.all()
        .annotate(rating=Avg('reviews__score'))
        .order_by('year', 'name')
    )
    permission_classes = (AdminLevelOrReadOnly,)
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter
    ordering_fields = ('id', 'name', 'year')
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('name', 'description')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializerWrite
        return TitleSerializerReadOnly


class ReviewViewSet(ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrModeratorLevelOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (OwnerOrModeratorLevelOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
