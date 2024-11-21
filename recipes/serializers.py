from rest_framework import serializers
from recipes.models import Recipe, Measurement, Ingredient, RecipeIngredient

class MeasurementSerializer(serializers.ModelSerializer):
    """Serializer for the Measurement model."""
    class Meta:
        model = Measurement
        fields = ['id', 'measure']


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for the Ingredient model."""
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for the RecipeIngredient model, to nest ingredient data."""
    ingredient = serializers.CharField()
    measure = serializers.CharField()

    class Meta:
            model = RecipeIngredient
            fields = ['id', 'recipe', 'ingredient', 'quantity', 'measure']

    # class Meta:
    #     model = RecipeIngredient
    #     fields = ['id', 'ingredient', 'quantity', 'measure']
    
    # def validate_recipe_ingredient(self, data):
    #     ingredient_name = data.get('ingredient')


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for the Recipe model, including nested ingredients."""
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size exceeds 2MB.'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image whidth is larger than 4096px'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096px'
            )
        return value 
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'recipe_name', 'intro', 'instruction',
            'image', 'recipe_ingredients'
        ]
       