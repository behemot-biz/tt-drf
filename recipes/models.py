from django.db import models
from django.contrib.auth.models import User


class Measurement(models.Model):
    """
    Measurement model for storing unit types (e.g., grams, cups, teaspoons).
    """
    measure = models.CharField(max_length=50, unique=True)  # e.g., "g", "cup", "ml"

    def __str__(self):
        return self.measure


class Ingredient(models.Model):
    """
    Ingredient model for storing common ingredients (e.g., water, sugar, flour).
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Recipe model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    recipe_name = models.CharField(max_length=255)
    intro = models.TextField(blank=True)
    instruction = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_lpzfbh', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.recipe_name}'


class RecipeIngredient(models.Model):
    """
    Intermediate model to store the relationship between Recipe and Ingredient,
    including the quantity and measurement.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient_recipes')
    quantity = models.CharField(max_length=50)
    measure = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.quantity} {self.measure} of {self.ingredient} for {self.recipe}'
