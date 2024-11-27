
from rest_framework import generics, permissions
from .models import Recipe, RecipeIngredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer
from tt_drf_api.permissions import IsOwnerOrReadOnly


class RecipeList(generics.ListCreateAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.all()


class RecipeIngredientList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = RecipeIngredientSerializer
    queryset = RecipeIngredient.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeIngredientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecipeIngredientSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = RecipeIngredient.objects.all()