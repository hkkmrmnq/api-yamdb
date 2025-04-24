from datetime import timezone

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True
    )

    genres = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=True
    )

    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)

    def get_rating(self, obj):
        try:
            reviews = obj.reviews.all()
            if reviews.exists():
                return round(
                    sum(review.score for review in reviews)
                    / reviews.count())
            return 0
        except ZeroDivisionError:
            return 0

    def validate(self, data):
        if 'year' in data and data['year'] > timezone.now().year:
            raise serializers.ValidationError(
                "Год не может быть в будущем.")
        return data

    def create(self, validated_data):
        genres_data = validated_data.pop('genres')
        title = Title.objects.create(**validated_data)
        title.genres.set(genres_data)
        return title

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'genres':
                instance.genres.set(value)
            elif attr == 'category':
                setattr(instance, attr, value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('title',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Нельзя повторно оставить отзыв на это произведение',
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('review',)
