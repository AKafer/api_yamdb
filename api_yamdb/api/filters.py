from django_filters import rest_framework as dfilters

from reviews.models import Title


class MyFilter(dfilters.FilterSet):
    name = dfilters.CharFilter(lookup_expr='icontains')
    genre = dfilters.CharFilter(field_name='genre__slug')
    category = dfilters.CharFilter(method='get_category_slug')

    def get_category_slug(self, queryset, name, value):
        queryset = queryset.filter(category__slug=value)
        return queryset

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
