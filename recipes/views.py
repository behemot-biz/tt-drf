from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Recipe, Measurement, Ingredient, RecipeIngredient
from .serializers import RecipeSerializer, RecipeIngredientSerializer
# , IngredientSerializer, MeasurementSerializer
from tt_drf_api.permissions import IsOwnerOrReadOnly


class RecipeList(APIView):
    """
    API view to retrieve all recipes.
    """
    serializer_class = RecipeSerializer

    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request}
        )
        return Response(serializer.data)
    
    def post(self, request):
        serializer = RecipeSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class RecipeIngredientListView(APIView):
    """
    API view to retrieve all recipe ingredients, 
    optionally filtered by recipe.
    """
    serializer_class = RecipeIngredientSerializer

    def get(self, request):
        recipe_id = request.query_params.get('recipe', None)
        if recipe_id:
            recipe_ingredients = RecipeIngredient.objects.filter(
                recipe_id=recipe_id
                )
        else:
            recipe_ingredients = RecipeIngredient.objects.all()
        serializer = RecipeIngredientSerializer(recipe_ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecipeIngredientSerializer(data=request.data)
        if serializer.is_valid():
            recipe_id = serializer.validated_data['recipe'].id
            ingredient_name = serializer.validated_data['ingredient']
            quantity = serializer.validated_data['quantity']
            measure_name = serializer.validated_data['measure']

            try:
                recipe = Recipe.objects.get(id=recipe_id)
            except Recipe.DoesNotExist:
                return Response({"error": "Recipe not found"}, status=status.HTTP_404_NOT_FOUND)
            
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            measure, _ = Measurement.objects.get_or_create(measure=measure_name)

            recipe_ingredient = RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=quantity,
                measure=measure
            )

            return Response(
                RecipeIngredientSerializer(recipe_ingredient).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
