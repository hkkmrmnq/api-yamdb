class CurrentTitleDefault:
    """Получает ID Произведения из URL"""

    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']

    def __repr__(self):
        return '%s()' % self.__class__.__name__
