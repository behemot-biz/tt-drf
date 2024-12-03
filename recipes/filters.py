from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Recipe, RecipeIngredient


class RecipeFilter(filters.FilterSet):
    """
    Custom filter for recipes, supporting filtering by owner, search terms,
    and creation date range.
    """
    recipe_name = filters.CharFilter(lookup_expr='icontains', label="Recipe Name")
    created_at = filters.DateFromToRangeFilter(label="Creation Date Range")
    owner = filters.CharFilter(field_name='owner__username', label="Owner")

    class Meta:
        model = Recipe
        fields = ['owner', 'recipe_name', 'created_at']


class RecipeIngredientFilter(filters.FilterSet):
    """
    FilterSet for filtering RecipeIngredient objects.
    - Allows filtering by the recipe ID, partial matches on the recipe name,
      and the ingredient name.

    Attributes:
        recipe: A NumberFilter for filtering by the exact ID of a recipe.
        recipe_name: CharFilter for case-insensitive partial matches on
            recipe name.
        ingredient: Filters RecipeIngredient by the related ingredient.

    Meta:
        model: The model to apply the filters to (`RecipeIngredient`).
        fields: The fields available for filtering
            (recipe, recipe_name, ingredient).
    """
    recipe = filters.NumberFilter(
        field_name='recipe__id',
        label="Recipe ID"
    )
    recipe_name = filters.CharFilter(
        field_name='recipe__recipe_name',
        lookup_expr='icontains',
        label="Recipe Name"
    )

    class Meta:
        model = RecipeIngredient
        fields = ['recipe', 'recipe_name', 'ingredient']
