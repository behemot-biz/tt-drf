
from django.db.models import Count
from rest_framework import generics, permissions, filters
from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer
from tt_drf_api.permissions import IsOwnerOrReadOnly


class RecipeList(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # queryset = Recipe.objects.all()
    queryset = Recipe.objects.annotate(
        likes_count = Count('likes', distinct=True),
        comments_count = Count('comment', distinct=True)
    ).order_by('created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.annotate(
        likes_count = Count('likes', distinct=True),
        comments_count = Count('comment', distinct=True)
    ).order_by('created_at')


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