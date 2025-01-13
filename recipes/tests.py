from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Ingredient, Measurement
from rest_framework import status
from rest_framework.test import APITestCase


class RecipeListViewTests(APITestCase):
    def setUp(self):
        self.kalle = User.objects.create_user(username='kalle', password='kula')
        self.other_user = User.objects.create_user(username='other_user', password='password')

    def test_can_list_recipes(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='a recipe name', status='published')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_logged_in_user_can_create_recipe(self):
        self.client.login(username='kalle', password='kula')
        response = self.client.post('/recipes/', {'recipe_name': 'a recipe name'})
        count = Recipe.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_recipe(self):
        response = self.client.post('/recipes/', {'recipe_name': 'a recipe name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_recipes_by_ingredient(self):
        recipe = Recipe.objects.create(owner=self.kalle, recipe_name='Pasta', status='published')
        ingredient = Ingredient.objects.create(name='Tomato')
        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity='1',
            measure=Measurement.objects.create(measure='kg')
        )

        response = self.client.get('/recipes/?search=Tomato')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['recipe_name'], 'Pasta')

    def test_pending_publish_visible_to_owner(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='Draft Recipe', status='pending_publish')
        self.client.login(username='kalle', password='kula')
        response = self.client.get('/recipes/?status=pending_publish')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pending_publish_not_visible_to_others(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='Draft Recipe', status='pending_publish')
        self.client.login(username='other_user', password='password')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_pending_delete_visible_to_owner(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='To Delete', status='pending_delete')
        self.client.login(username='kalle', password='kula')
        response = self.client.get('/recipes/?status=pending_delete')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pending_delete_not_visible_to_others(self):
        Recipe.objects.create(owner=self.kalle, recipe_name='To Delete', status='pending_delete')
        self.client.login(username='other_user', password='password')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class RecipeDetailViewTests(APITestCase):
    def setUp(self):
        self.kalle = User.objects.create_user(username='kalle', password='kula')
        self.other_user = User.objects.create_user(username='other_user', password='password')
        self.recipe = Recipe.objects.create(owner=self.kalle, recipe_name='Test Recipe')

    def test_can_retrieve_recipe(self):
        self.recipe.status = 'published'
        self.recipe.save()
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
        self.recipe.status = 'published'
        self.recipe.save()
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
        self.recipe.status = 'published'
        self.recipe.save()
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
