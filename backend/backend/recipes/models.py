# from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='тэги',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientRecipe',
        related_name='recipes',
        verbose_name='ингредиенты',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/%Y/%m/%d',
        verbose_name='изображение',
    )
    text = models.TextField(
        verbose_name='описание рецепта'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(1),
        ],
        verbose_name='время приготовления',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def in_favourite_count(self):
        return self.favourite.count()
    in_favourite_count.short_description = 'Количество добавлений в избранное'


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='название тэга',
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='цвет HEX'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                r'^[-a-zA-Z0-9_]+$',
                message='Slug может содержать латинские буквы, цифры и знак _',
            )
        ],
        verbose_name='слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='единицы измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиенты',
        related_name='ingredient_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
    )
    amount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
        ],
        default=1,
        verbose_name='количество ингредиента'
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_fields',
            ),
        )
        ordering = ('recipe',)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique fields',
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='subscribe to yourself',
            ),
        ]

    def folower_count(self):
        return self.user.following.count()
    folower_count.short_description = 'Количество подписок'

    def folowing_count(self):
        return self.user.follower.count()
    folowing_count.short_description = 'Количество подписчиков'


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_recipes',
        verbose_name='Автор избранного'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favourite',
        verbose_name='Избранные рецепты',
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Список избранных рецептов'
        verbose_name_plural = 'Списки избранных рецептов'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_user_recipe',
            ),
        )

    def __str__(self):
        return (f'{self.user.username}, '
                f'в избранном рецептов: {self.recipes_count}')

    def recipes_count(self):
        return self.user.favourite_recipes.count()
    recipes_count.short_description = 'Количество в избранном'
