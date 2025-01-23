from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Ingredient, Measurement
from rest_framework import status
from rest_framework.test import APITestCase


class RecipeListViewTests(APITestCase):
    """
    Test cases for listing, creating, and searching recipes via the API.
    """

    def setUp(self):
        """
        Create test users and set up initial data for the tests.
        """
        self.kalle = User.objects.create_user(
            username='kalle', password='kula')
        self.other_user = User.objects.create_user(
                username='other_user', password='password')

    def test_can_list_recipes(self):
        """
        Test that the API can list all recipes.
        """
        Recipe.objects.create(
            owner=self.kalle, recipe_name='a recipe name', status='published')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_logged_in_user_can_create_recipe(self):
        """
        Test that a logged-in user can create a new recipe.
        """
        self.client.login(username='kalle', password='kula')
        response = self.client.post(
            '/recipes/', {'recipe_name': 'a recipe name'})
        count = Recipe.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_recipe(self):
        """
        Test that an unauthenticated user cannot create a recipe.
        """
        response = self.client.post(
            '/recipes/', {'recipe_name': 'a recipe name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_recipes_by_ingredient(self):
        """
        Test searching for recipes by ingredient.
        """
        recipe = Recipe.objects.create(
            owner=self.kalle, recipe_name='Pasta', status='published')
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
        """
        Test that recipes with a 'pending_publish' status are visible only
        to their owner.
        """
        Recipe.objects.create(
            owner=self.kalle,
            recipe_name='Draft Recipe', status='pending_publish')
        self.client.login(username='kalle', password='kula')
        response = self.client.get('/recipes/?status=pending_publish')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pending_publish_not_visible_to_others(self):
        """
        Test that recipes with a 'pending_publish' status are not visible
        to other users.
        """
        Recipe.objects.create(
            owner=self.kalle, recipe_name='Draft Recipe',
            status='pending_publish')
        self.client.login(username='other_user', password='password')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_pending_delete_visible_to_owner(self):
        """
        Test that recipes with a 'pending_delete' status are
        visible only to their owner.
        """
        Recipe.objects.create(
                owner=self.kalle, recipe_name='To Delete',
                status='pending_delete')
        self.client.login(username='kalle', password='kula')
        response = self.client.get('/recipes/?status=pending_delete')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_pending_delete_not_visible_to_others(self):
        """
        Test that recipes with a 'pending_delete' status are not
        visible to other users.
        """
        Recipe.objects.create(owner=self.kalle,
                              recipe_name='To Delete', status='pending_delete')
        self.client.login(username='other_user', password='password')
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class RecipeDetailViewTests(APITestCase):
    """
    Test cases for retrieving, updating, and deleting a single recipe.
    """

    def setUp(self):
        """
        Create test users and a sample recipe for the tests.
        """
        self.kalle = User.objects.create_user(
            username='kalle', password='kula')
        self.other_user = User.objects.create_user(
            username='other_user', password='password')
        self.recipe = Recipe.objects.create(
                owner=self.kalle, recipe_name='Test Recipe')

    def test_can_retrieve_recipe(self):
        """
        Test that a recipe can be retrieved by its ID.
        """
        self.recipe.status = 'published'
        self.recipe.save()
        response = self.client.get(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['recipe_name'], 'Test Recipe')

    def test_logged_in_user_can_update_own_recipe(self):
        """
        Test that a logged-in user can update their own recipe.
        """
        self.client.login(username='kalle', password='kula')
        response = self.client.put(
                f'/recipes/{self.recipe.id}/',
                {'recipe_name': 'Updated Recipe'})
        self.recipe.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.recipe.recipe_name, 'Updated Recipe')

    def test_logged_in_user_cannot_update_other_users_recipe(self):
        """
        Test that a logged-in user cannot update another user's recipe.
        """
        self.recipe.status = 'published'
        self.recipe.save()
        self.client.login(username='other_user', password='password')
        response = self.client.put(
            f'/recipes/{self.recipe.id}/',
            {'recipe_name': 'Updated Recipe'})
        self.recipe.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.recipe.recipe_name, 'Updated Recipe')

    def test_logged_in_user_can_delete_own_recipe(self):
        """
        Test that a logged-in user can delete their own recipe.
        """
        self.client.login(username='kalle', password='kula')
        response = self.client.delete(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Recipe.objects.count(), 0)

    def test_logged_in_user_cannot_delete_other_users_recipe(self):
        """
        Test that a logged-in user cannot delete another user's recipe.
        """
        self.recipe.status = 'published'
        self.recipe.save()
        self.client.login(username='other_user', password='password')
        response = self.client.delete(f'/recipes/{self.recipe.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Recipe.objects.count(), 1)


class RecipeIngredientViewTests(APITestCase):
    """
    Test cases for managing recipe ingredients via the API.
    """

    def setUp(self):
        """
        Create test users, a sample recipe, and ingredients for the tests.
        """
        self.kalle = User.objects.create_user(
            username='kalle', password='kula')
        self.recipe = Recipe.objects.create(
                owner=self.kalle, recipe_name='Test Recipe')
        self.ingredient = Ingredient.objects.create(name='Sugar')
        self.measurement = Measurement.objects.create(measure='grams')

    def test_logged_in_user_can_add_ingredient_to_own_recipe(self):
        """
        Test that a logged-in user can add ingredients to their own recipe.
        """
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
        """
        Test that a logged-in user cannot add ingredients to another
        user's recipe.
        """
        other_user = User.objects.create_user(
            username='other_user', password='password')
        other_recipe = Recipe.objects.create(
            owner=other_user, recipe_name='Other Recipe')
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
        """
        Test that a logged-in user can delete ingredients from
        their own recipe.
        """
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
