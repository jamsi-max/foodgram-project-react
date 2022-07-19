from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class BasketUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='basket',
        verbose_name='Покупатель'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='basket_recipe',
        verbose_name='Рецепты в корзине'
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='basket_unique_user_recipe',
            ),
        )

    def recipes_count(self):
        return self.user.basket.count()
    recipes_count.short_description = 'Количество добавленных рецептов'
