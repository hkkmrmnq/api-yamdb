from django.core.exceptions import ValidationError
import re


def validate_username(username):
    """
    Валидатор для username.
    Проверка на соответствие правилам:
    - разрешены только латинские буквы, цифры и символы:
    ., @, +, -, _
    - запрещено использование 'me' в качестве username.
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
