import string
from random import choices

from django.conf import settings
from django.core.cache import cache


def create_confirmation_code(email, length=6):
    """
    1. Генерирует случайный код подтверждения,
    2. сохраняет в кэш под ключом confirmation_code_{email},
    3. возвращает сгенерированный код.
    """
    confirmation_code = ''.join(choices(string.digits, k=6))
    cache.set(
        f'confirmation_code_{email}',
        str(confirmation_code),
        settings.CACHE_TIMEOUT,
    )
    return ''.join(confirmation_code)
