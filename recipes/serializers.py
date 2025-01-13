from rest_framework import serializers
from .models import Recipe, Measurement, Ingredient, RecipeIngredient
from likes.models import Like


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Measurement model.
    Serializes fields required for measurement units (e.g., grams, cups, etc.).
    """
    class Meta:
        model = Measurement
        fields = ['id', 'measure']


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.
    Serializes fields required for ingredient names (e.g., sugar, flour, etc.).
    """
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the RecipeIngredient model.
    - Handles the nesting of ingredient and measurement data.
    - Allows converting string values for ingredient and measurement into
      related instances.
    - Ensures only recipe owners can modify ingredients.

    Fields:
        - `id`: Unique identifier for the ingredient entry.
        - `recipe`: ForeignKey to the associated recipe.
        - `ingredient`: Name of the ingredient (string or nested object).
        - `quantity`: Quantity of the ingredient (e.g., "200" for 200 grams).
        - `measure`: Unit of measurement (e.g., "grams", "cups").
        - `is_owner`: Indicates if the logged-in user owns the recipe.
        - `owner`: Username of the recipe owner.

    Methods:
        - `get_is_owner`: Checks if the logged-in user is the owner of the
            recipe.
        - `validate`: Ensures valid ownership and converts nested data for
            ingredient and measurement.
        - `create`: Creates a new RecipeIngredient instance.
        - `update`: Updates an existing RecipeIngredient instance.
    """
    ingredient = serializers.CharField()  # Accept ingredient name as a string
    measure = serializers.CharField()  # Accept measure name as a string
    owner = serializers.ReadOnlyField(source='recipe.owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Determines if the logged-in user is the owner of the recipe.

        Args:
            obj (RecipeIngredient): The instance of RecipeIngredient
            being checked.

        Returns:
            bool: True if the user owns the recipe, False otherwise.
        """
        if isinstance(obj, RecipeIngredient):
            request = self.context['request']
            return request.user == obj.recipe.owner
        return False

    def validate(self, data):
        """
        Validates ownership of the recipe and converts ingredient/measurement
        names to model instances.

        Args:
            data (dict): Data to be validated.

        Raises:
            serializers.ValidationError: If the logged-in user does not own
            the recipe.

        Returns:
            dict: Validated data with ingredient and measure instances.
        """
        recipe = data.get('recipe')
        request = self.context['request']

        # Ensure user owns the recipe
        if recipe.owner != request.user:
            raise serializers.ValidationError(
                "You are not authorized to modify this recipe."
            )

        # Convert ingredient and measurement names to instances
        ingredient_name = data.get('ingredient')
        measure_name = data.get('measure')

        ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
        measure, _ = Measurement.objects.get_or_create(measure=measure_name)

        # Replace string data with instances
        data['ingredient'] = ingredient
        data['measure'] = measure

        return data

    def create(self, validated_data):
        """
        Creates a new RecipeIngredient instance after validation.

        Args:
            validated_data (dict): Validated data for the new instance.

        Returns:
            RecipeIngredient: The newly created instance.
        """
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Updates an existing RecipeIngredient instance.

        Args:
            instance (RecipeIngredient): The instance being updated.
            validated_data (dict): Validated data for the update.

        Returns:
            RecipeIngredient: The updated instance.
        """
        # Handle updates for nested fields
        if 'ingredient' in validated_data:
            ingredient_name = validated_data.pop('ingredient')
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_name
                )
            instance.ingredient = ingredient

        if 'measure' in validated_data:
            measure_name = validated_data.pop('measure')
            measure, _ = Measurement.objects.get_or_create(
                measure=measure_name
                )
            instance.measure = measure

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = RecipeIngredient
        fields = [
            'id', 'recipe', 'ingredient', 'quantity', 'measure',
            'is_owner', 'owner'
            ]


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe model.
    - Provides detailed representation of recipe data.
    - Includes nested recipe ingredients data.
    - Ensures only the recipe owner can make updates.

    Fields:
        - `id`: Unique identifier for the recipe.
        - `recipe_name`: Name of the recipe.
        - `image`: Recipe image (optional).
        - `intro`: Short introduction or description of the recipe.
        - `instruction`: Detailed instructions for the recipe.
        - `owner`: Username of the recipe owner.
        - `profile_id`: ID of the owner's profile (for frontend linking).
        - `profile_image`: URL of the owner's profile image.
        - `recipe_ingredients`: Nested list of associated ingredients.
        - `status`: Recipe status, default value is pending_publish.
        - `created_at`: Timestamp for when the recipe was created.
        - `updated_at`: Timestamp for when the recipe was last updated.
        - `is_owner`: Indicates if the logged-in user owns the recipe.

    Methods:
        - `get_is_owner`: Checks if the logged-in user is the owner of
            the recipe.
        - `validate_image`: Ensures uploaded image meets size and resolution
            constraints.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    status = serializers.ChoiceField(  # Add status field
        choices=[
            ("pending_publish", "Pending Publish"),
            ("published", "Published"),
            ("pending_delete", "Pending Delete"),
        ],
        required=False,
    )

    def validate_image(self, value):
        """
        Validates uploaded image size and dimensions.

        Args:
            value (ImageField): The uploaded image.

        Raises:
            serializers.ValidationError: If the image exceeds size or
            dimension limits.

        Returns:
            ImageField: The validated image.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size exceeds 2MB.'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width is larger than 4096px.'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height is larger than 4096px.'
            )
        return value

    def get_is_owner(self, obj):
        """
        Determines if the logged-in user is the owner of the recipe.

        Args:
            obj (Recipe): The Recipe instance being checked.

        Returns:
            bool: True if the user owns the recipe, False otherwise.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, recipe=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Recipe
        fields = [
            'id', 'recipe_name', 'image', 'intro', 'instruction',
            'owner', 'profile_id', 'recipe_ingredients',
            'created_at', 'updated_at', 'is_owner', 'like_id',
            'likes_count', 'comments_count', 'status',
        ]
