from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Comment, Recipe


class CommentTests(APITestCase):
    """
    Test cases for Comment model, serializer, and views.
    """

    def setUp(self):
        # Create users
        self.user = User.objects.create_user(
            username="kalle", password="kula"
            )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass"
            )

        # Create a recipe
        self.recipe = Recipe.objects.create(
            owner=self.user, recipe_name="Test Recipe"
            )

        # Create a comment
        self.comment = Comment.objects.create(
            owner=self.user,
            recipe=self.recipe,
            content="This is a test comment"
        )

    def test_list_comments(self):
        """
        Ensure all comments are listed.
        """
        response = self.client.get("/comments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]["content"],
                         "This is a test comment")

    def test_create_comment_authenticated(self):
        """
        Ensure an authenticated user can create a comment.
        """
        self.client.login(username="kalle", password="kula")
        data = {"recipe": self.recipe.id, "content": "Another test comment"}
        response = self.client.post("/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(response.data["content"], "Another test comment")

    def test_create_comment_unauthenticated(self):
        """
        Ensure an unauthenticated user cannot create a comment.
        """
        data = {"recipe": self.recipe.id, "content": "Unauthorized comment"}
        response = self.client.post("/comments/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_comment(self):
        """
        Ensure a single comment can be retrieved.
        """
        response = self.client.get(f"/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "This is a test comment")

    def test_update_comment_owner(self):
        """
        Ensure the owner can update their comment.
        """
        self.client.login(username="kalle", password="kula")
        data = {"content": "Updated comment"}
        response = self.client.put(f"/comments/{self.comment.id}/", data)
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment.content, "Updated comment")

    def test_update_comment_non_owner(self):
        """
        Ensure a non-owner cannot update the comment.
        """
        self.client.login(username="otheruser", password="otherpass")
        data = {"content": "Hacked comment"}
        response = self.client.put(f"/comments/{self.comment.id}/", data)
        self.comment.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.comment.content, "Hacked comment")

    def test_delete_comment_owner(self):
        """
        Ensure the owner can delete their comment.
        """
        self.client.login(username="kalle", password="kula")
        response = self.client.delete(f"/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_delete_comment_non_owner(self):
        """
        Ensure a non-owner cannot delete the comment.
        """
        self.client.login(username="otheruser", password="otherpass")
        response = self.client.delete(f"/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), 1)
