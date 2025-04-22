from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnly
from .serializers import ReviewSerializer, UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


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
        serializer.save(
            author=self.request.user,
            title=title
        )
