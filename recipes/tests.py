from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Ingredient, Measurement
from rest_framework import status
from rest_framework.test import APITestCase


class RecipeListViewTests(APITestCase):
    def setUp(self):
        self.kalle = User.objects.create_user(username='kalle', password='kula')
        self.other_user = User.objects.create_user(username='other_user', password='password')

    def test_can_list_recipes(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='a recipe name')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_logged_in_user_can_create_recipe(self):
        self.client.login(username='kalle', password='kula')
        response = self.client.post('/recipes/', {'recipe_name': 'a recipe name'})
        count = Recipe.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_recipe(self):
        response = self.client.post('/recipes/', {'recipe_name': 'a recipe name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_recipe_list_filtered_by_owner(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='Recipe 1')
        Recipe.objects.create(owner=self.other_user, recipe_name='Recipe 2')
        response = self.client.get(f'/recipes/?owner={self.kalle.id}')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['recipe_name'], 'Recipe 1')


class RecipeDetailViewTests(APITestCase):
    def setUp(self):
        self.kalle = User.objects.create_user(username='kalle', password='kula')
        self.other_user = User.objects.create_user(username='other_user', password='password')
        self.recipe = Recipe.objects.create(owner=self.kalle, recipe_name='Test Recipe')

    def test_can_retrieve_recipe(self):
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe_name'], 'Test Recipe')

    def test_logged_in_user_can_update_own_recipe(self):
        self.client.login(username='kalle', password='kula')
        response = self.client.put(f'/recipes/{self.recipe.id}/', {'recipe_name': 'Updated Recipe'})
        self.recipe.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.recipe.recipe_name, 'Updated Recipe')

    def test_logged_in_user_cannot_update_other_users_recipe(self):
        self.client.login(username='other_user', password='password')
        response = self.client.put(f'/recipes/{self.recipe.id}/', {'recipe_name': 'Updated Recipe'})
        self.recipe.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.recipe.recipe_name, 'Updated Recipe')

    def test_logged_in_user_can_delete_own_recipe(self):
        self.client.login(username='kalle', password='kula')
        response = self.client.delete(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_logged_in_user_cannot_delete_other_users_recipe(self):
        self.client.login(username='other_user', password='password')
        response = self.client.delete(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.count(), 1)


class RecipeIngredientViewTests(APITestCase):
    def setUp(self):
        self.kalle = User.objects.create_user(username='kalle', password='kula')
        self.recipe = Recipe.objects.create(owner=self.kalle, recipe_name='Test Recipe')
        self.ingredient = Ingredient.objects.create(name='Sugar')
        self.measurement = Measurement.objects.create(measure='grams')

    def test_logged_in_user_can_add_ingredient_to_own_recipe(self):
        self.client.login(username='kalle', password='kula')
        data = {
            'recipe': self.recipe.id,
            'ingredient': 'Salt',
            'quantity': '5',
            'measure': 'grams'
        }
        response = self.client.post('/ingredients/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RecipeIngredient.objects.count(), 1)

    def test_logged_in_user_cannot_add_ingredient_to_other_users_recipe(self):
        other_user = User.objects.create_user(username='other_user', password='password')
        other_recipe = Recipe.objects.create(owner=other_user, recipe_name='Other Recipe')
        self.client.login(username='kalle', password='kula')
        data = {
            'recipe': other_recipe.id,
            'ingredient': 'Salt',
            'quantity': '5',
            'measure': 'grams'
        }
        response = self.client.post('/ingredients/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecipeIngredient.objects.count(), 0)

    def test_logged_in_user_can_delete_own_recipe_ingredient(self):
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity='5',
            measure=self.measurement
        )
        self.client.login(username='kalle', password='kula')
        response = self.client.delete(f'/ingredients/{recipe_ingredient.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RecipeIngredient.objects.count(), 0)
