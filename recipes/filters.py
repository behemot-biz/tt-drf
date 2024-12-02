from django_filters import rest_framework as filters
from .models import Recipe, RecipeIngredient


class RecipeFilter(filters.FilterSet):
    """
    FilterSet for filtering Recipe objects.
    - Allows filtering by recipe owner, partial matches on recipe name,
      and a date range for creation.

    Attributes:
        recipe_name: A CharFilter for case-insensitive partial matches on
            the recipe name.
        created_at: A DateFromToRangeFilter for filtering recipes by a
            date range.

    Meta:
        model: The model to apply the filters to (`Recipe`).
        fields: The fields available for filtering (owner, recipe_name,
            created_at).
    """
    
    recipe_name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter(label="Create Date Range")

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
