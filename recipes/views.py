from django.db.models import Count, Q
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer
from tt_drf_api.permissions import IsOwnerOrReadOnly

"""
Views for the Recipe app.

This module provides API views for managing recipes and their ingredients,
allowing users to create, update, delete, and retrieve data. The views are
designed with permissions to ensure proper access control and include
support for filtering, searching, and ordering.

Classes:
    - RecipeList: Handles listing and creation of recipes. Supports filters,
      search, and ordering for published recipes, while authenticated users
      can manage their own drafts and deletions.
    - RecipeDetail: Provides detailed view of a recipe, allowing owners to
      update or delete their recipes. Handles access control based on recipe
      ownership and status.
    - RecipeIngredientList: Manages listing and creation of recipe ingredients.
      Ensures that only recipe owners can add ingredients to their recipes.
    - RecipeIngredientDetail: Provides detail, update, and delete operations
      for a specific recipe ingredient. Restricted to the recipe owner.
"""


class RecipeList(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'status',  # Add status as a filterable field
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'recipe_name',
        'recipe_ingredients__ingredient__name',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def get_queryset(self):
        """
        Return recipes based on query parameters.
        """
        queryset = Recipe.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True)
        ).order_by('-created_at')

        status_filter = self.request.query_params.getlist('status')  # Fetch as list
        if status_filter:
            queryset = queryset.filter(status__in=status_filter)  # Use __in for multiple values

        # Otherwise, default to showing only published recipes
        else:
            queryset = queryset.filter(status='published')

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, status='pending_publish')


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # queryset = Recipe.objects.annotate(
    #     likes_count=Count('likes', distinct=True),
    #     comments_count=Count('comment', distinct=True)
    # ).order_by('created_at')

    def get_queryset(self):
        """
        Return recipes based on query parameters and ownership.
        """
        user = self.request.user
        queryset = Recipe.objects.annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comment', distinct=True)
        ).order_by('created_at')

        if user.is_authenticated:
            return queryset.filter(
                Q(status='published') |
                Q(status__in=['pending_publish', 'pending_delete'], owner=user)
            )

        return queryset.filter(status='published')


class RecipeIngredientList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()

    def perform_create(self, serializer):
        recipe = serializer.validated_data.get('recipe')
        # Check if the logged-in user is the owner of the recipe
        if recipe.owner != self.request.user:
            raise serializer.ValidationError(
                "You cannot add ingredients to recipes you do not own."
            )
        serializer.save()


class RecipeIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = RecipeIngredient.objects.all()
