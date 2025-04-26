from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

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

        read_only_fields = ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sender = self.context['request'].user
        if sender.is_authenticated and (
            sender.is_superuser or sender.role == 'admin'
        ):
            self.fields['role'].read_only = False

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                '"me" - недопустимое имя пользователя.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
