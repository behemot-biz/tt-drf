from django.db import models
from django.contrib.auth.models import User
from recipes.models import Recipe


class Like(models.Model):
    """
    Model to represent a 'like' for a recipe.

    Attributes:
    - owner: The user who liked the recipe.
    - recipe: The recipe that has been liked.
    - created_at: Timestamp of when the like was created.

    Constraints:
    - A user can like a specific recipe only once (unique_together constraint).
    - Likes are ordered by the most recent first (ordering by '-created_at').
    """
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
        )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="likes",
        )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'recipe']

    def __str__(self):
        return f'{self.owner} {self.recipe}'
