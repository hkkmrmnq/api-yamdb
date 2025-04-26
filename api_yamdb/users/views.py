from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action, api_view
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import AccessToken

from .emails import send_confirmation_email
from .mixins import PartialUpdateMixin
from .serializers import TokenSerializer, UserSerializer
from .utils import create_confirmation_code
from api.permissions import AdminLevel

User = get_user_model()


class UserViewSet(
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    PartialUpdateMixin,
    GenericViewSet,
):
    """Вьюсет для модели пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'
    filter_backends = (DjangoFilterBackend, SearchFilter)
    permission_classes = (AdminLevel,)
    filterset_fields = ('first_name', 'last_name', 'role')
    search_fields = ('username', 'first_name', 'last_name')

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        """
        Эндпоинт '/v1/users/me/':
        - GET: просмотр данных своей учетной записи.
        - PATCH: редактирование данных своей учетной записи, кроме поля 'role'.
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    request_username = request.data.get('username')
    request_user = User.objects.filter(username=request_username)
    request_email = request.data.get('email')
    if request_user.exists():
        user = request_user.first()
        if user.email != request_email:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        confirmation_code = create_confirmation_code(user.email)
        send_confirmation_email(user.email, confirmation_code)
        user.is_active = False
        user.save()
        return Response(
            {'email': user.email, 'username': user.username},
            status=status.HTTP_200_OK,
        )
    serializer = UserSerializer(
        data=request.data, context={'request': request}
    )
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        confirmation_code = create_confirmation_code(email)
        serializer.save(is_active=False, role='user')
        send_confirmation_email(email, confirmation_code)
        return Response(
            {
                'email': email,
                'username': username,
            },
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def generate_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        expected_code = cache.get(f'confirmation_code_{user.email}')
        if expected_code == confirmation_code:
            user.is_active = True
            user.save()
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'message': 'Код подтверждения недействителен.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
