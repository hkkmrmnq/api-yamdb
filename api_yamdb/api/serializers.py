from datetime import datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


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


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
            'rating',
        )
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(obj.rating)
        return None

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError('Год не может быть в будущем.')
        return value

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError('Необходимо указать жанр')
        return value

    def validate_category(self, value):
        if not value:
            raise serializers.ValidationError('Необходимо указать категорию')
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre.all(), many=True
        ).data
        return representation


class CurrentTitleDefault:
    """Получает ID Произведения из URL"""

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']

    def __repr__(self):
        return '%s()' % self.__class__.__name__


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
