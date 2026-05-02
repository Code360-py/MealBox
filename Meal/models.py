from django.db import models
from django.contrib.auth.models import User


class Bookmark(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )
    meal_id = models.CharField(
        max_length=100
    )  # TheMealDB meal ID
    meal_name = models.CharField(
        max_length=255
    )
    meal_thumb = models.URLField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'meal_id')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.meal_name}"