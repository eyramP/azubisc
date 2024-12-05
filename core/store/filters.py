import django_filters as filters

from .models import Product


class ProductsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    price = filters.NumberFilter()
    price__gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'min_price']


class CategoryFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name='name', lookup_expr='icontains')

