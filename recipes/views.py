from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from tt_drf_api.permissions import IsOwnerOrReadOnly
from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer
from .filters import RecipeFilter, RecipeIngredientFilter


class RecipeList(generics.ListCreateAPIView):
    """
    API view for listing and creating recipes.
    - Allows all users to view recipes.
    - Only authenticated users can create new recipes.
    - Filters are applied using `RecipeFilter`.

    Attributes:
        serializer_class: The serializer class for recipes.
        permission_classes: Permissions required for accessing the view.
        queryset: Queryset of all recipes.
        filter_backends: Backend used for filtering.
        filterset_class: The filterset class used for filtering recipes.

    Methods:
        perform_create: Assigns logged-in user as owner when creating a recipe.
    """
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """
        Assigns the logged-in user as the owner of the recipe during creation.

        Args:
            serializer: The serializer instance used for saving the recipe.
        """
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific recipe.
    - Only the recipe owner can update or delete their recipe.

    Attributes:
        serializer_class: The serializer class for recipes.
        permission_classes: Permissions required for accessing the view.
        queryset: Queryset of all recipes.
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()


class RecipeIngredientList(generics.ListCreateAPIView):
    """
    API view for listing and creating recipe ingredients.
    - Allows all users to view recipe ingredients.
    - Only authenticated users can add ingredients to their own recipes.
    - Filters are applied using `RecipeIngredientFilter`.

    Attributes:
        serializer_class: The serializer class for recipe ingredients.
        permission_classes: Permissions required for accessing the view.
        queryset: Queryset of all recipe ingredients.
        filter_backends: Backend used for filtering.
        filterset_class: Filterset class for filtering recipe ingredients.

    Methods:
        perform_create: Ensures that only the recipe owner can add ingredients.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeIngredientFilter

    def perform_create(self, serializer):
        """
        Ensures that only the owner of the recipe can add ingredients to it.

        Args:
            serializer: Serializer instance used for saving recipe ingredient.

        Raises:
            ValidationError: If the logged-in user is not the owner of recipe.
        """
        recipe = serializer.validated_data.get('recipe')
        # Check if the logged-in user is the owner of the recipe
        if recipe.owner != self.request.user:
            raise serializer.ValidationError(
                "You cannot add ingredients to recipes you do not own."
            )
        serializer.save()


class RecipeIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a specific recipe
    ingredient.
    - Only the recipe owner can update or delete recipe ingredients.

    Attributes:
        serializer_class: The serializer class for recipe ingredients.
        permission_classes: Permissions required for accessing the view.
        queryset: Queryset of all recipe ingredients.
    """
    serializer_class = RecipeIngredientSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = RecipeIngredient.objects.all()
