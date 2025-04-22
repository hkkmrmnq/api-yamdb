from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .permissions import IsAuthorOrReadOnly
from .serializers import ReviewSerializer

from reviews.models import Title


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
