from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe

User = get_user_model()


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        lookup_expr='contains',
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited', 'author', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                favourite__user=self.request.user,
            ).prefetch_related('ingredients')
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(
                basket_recipe__user=self.request.user
            ).prefetch_related('ingredients')
        return queryset
