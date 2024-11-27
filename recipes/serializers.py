from rest_framework import serializers
from .models import Recipe, Measurement, Ingredient, RecipeIngredient


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
    owner = serializers.ReadOnlyField(source='recipe.owner.username')
    is_owner = serializers.SerializerMethodField()
    
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.recipe.owner
    
    class Meta:
            model = RecipeIngredient
            fields = ['id', 'recipe', 'ingredient', 'quantity', 'measure', 'is_owner', 'owner']


class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)

    
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

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner


    class Meta:
        model = Recipe
        fields = [
            'id', 'recipe_name', 'image', 'intro', 'instruction','owner', 
            'profile_id', 'profile_image', 'recipe_ingredients',
            'created_at', 'updated_at', 'is_owner'
        ]

