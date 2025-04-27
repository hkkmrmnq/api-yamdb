from django_filters import CharFilter, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """Filterset для возможности фильтрации произведений по идентификатору."""

    genre = CharFilter(
        field_name='genre__slug', lookup_expr='exact'
    )
    category = CharFilter(
        field_name='category__slug', lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
