from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .emails import send_confirmation_email
from .utils import CurrentTitleDefault
from reviews.constants import EMAIL_MAX_LENGTH
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_username

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializerReadOnly(serializers.ModelSerializer):
    """Сериализатор данных модели произведения для чтения."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(obj.rating)
        return None


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', required=True
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_null=False,
        allow_empty=False,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
        )

    def to_representation(self, instance):
        return TitleSerializerReadOnly(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    title = serializers.HiddenField(
        default=CurrentTitleDefault(),
    )

    class Meta:
        fields = ('id', 'title', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('author', 'title', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Нельзя повторно оставить отзыв на это произведение',
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class AdiminUserSerializer(serializers.ModelSerializer):
    """Админский сериализатор для работы с объектами пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserSerializer(AdiminUserSerializer):
    """Пользовательский сериализатор для работы с объектами пользователя."""

    class Meta(AdiminUserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        required=True, validators=[validate_username]
    )
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if len(value) > EMAIL_MAX_LENGTH:
            raise serializers.ValidationError(
                'Длина email не должна превышать 254 символа'
            )
        return value

    def validate(self, data):
        if User.objects.filter(
            (Q(username=data['username']) & ~Q(email=data['email']))
            | (Q(email=data['email']) & ~Q(username=data['username']))
        ).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email/username уже существует'
            )
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.is_active = False
        user.save()
        account_activation_token = default_token_generator.make_token(user)
        send_confirmation_email(user.email, account_activation_token)
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(
        required=True, validators=[validate_username]
    )
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                'Токен для активации недействителен.'
            )
        return data

    def create(self, validated_data):
        user = get_object_or_404(User, username=validated_data['username'])
        user.is_active = True
        user.save()
        return user
