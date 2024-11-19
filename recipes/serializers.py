from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

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
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'recipe_name', 'intro', 'ingredients', 'instruction',
            'image'
        ]