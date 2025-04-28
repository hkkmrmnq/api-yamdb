from rest_framework import serializers

from reviews.constants import USERNAME_MAX_LENGTH
from users.validators import validate_username


class UsernameFieldMixin(serializers.Serializer):
    """Миксин для поля username."""

    username = serializers.CharField(
        required=True,
        validators=[validate_username],
        max_length=USERNAME_MAX_LENGTH
    )
