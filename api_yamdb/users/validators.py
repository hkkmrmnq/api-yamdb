from django.core.exceptions import ValidationError
import re

from reviews.constants import USERNAME_MAX_LENGTH


def validate_username(username):
    """
    Валидатор для username.
    Проверка на соответствие ^[\w.@+-]+\Z
    и запрет использования 'me' в качестве username.
    """
    allowed_pattern = r'[\w.@+-]'

    non_matching_characters = re.sub(allowed_pattern, '', username)

    if non_matching_characters:
        formatted_invalid_chars = ", ".join(
            f"'{char}'" for char in non_matching_characters
        )
        raise ValidationError(
            f'Символы: {formatted_invalid_chars} не разрешены.'
        )
    elif username == "me":
        raise ValidationError(
            "Использовать 'me' в качестве username запрещено."
        )
    elif len(username) > USERNAME_MAX_LENGTH:
        raise ValidationError(
            (
                'Длина username не должна превышать '
                f'{USERNAME_MAX_LENGTH} символов.'
            )
        )
