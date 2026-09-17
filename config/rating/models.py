from django.db import models
from django.conf import settings
from menu.models import MenuItem


class Rating(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    rating = models.PositiveSmallIntegerField()

    review = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'menu_item'],
                name='unique_user_menu_item_rating'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.menu_item} - {self.rating}"

# Create your models here.
