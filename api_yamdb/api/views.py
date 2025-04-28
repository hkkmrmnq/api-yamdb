from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

# from .emails import send_confirmation_email
from .filters import TitleFilter
from .permissions import (
    AdminLevel,
    AdminLevelOrReadOnly,
    OwnerOrModeratorLevelOrReadOnly,
)
from .serializers import (
    AdiminUserSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializerReadOnly,
    TitleSerializerWrite,
    SignUpSerializer,
    TokenSerializer,
    UserSerializer,
)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


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


class UserViewSet(ModelViewSet):
    """Вьюсет для модели пользователя."""

    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = AdiminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (AdminLevel,)
    filterset_fields = ('first_name', 'last_name', 'role')
    search_fields = ('username', 'first_name', 'last_name')


@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def me(request):
    """
    Эндпоинт '/v1/users/me/':
    - GET: просмотр данных своей учетной записи.
    - PATCH: редактирование данных своей учетной записи, кроме поля 'role'.
    """
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def activate_account(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    access_token = AccessToken.for_user(user)
    return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
