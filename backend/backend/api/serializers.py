from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from recipes.models import (FavouriteRecipe,
                            Follow,
                            Ingredient,
                            IngredientRecipe,
                            Recipe,
                            Tag,)

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id',
                  'name',
                  'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(
        source='ingredient.name'
    )
    measurement_unit= serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id',
                  'name',
                  'measurement_unit',
                  'amount',)
        validators = (
            UniqueTogetherValidator(
                queryset=IngredientRecipe.objects.all(),
                fields=('ingredient', 'recipe')
            ),
        )
        read_only_fields = ('id', )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',
                  'name',
                  'color',
                  'slug')


class FoodUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if user and user.is_authenticated:
            return Follow.objects.filter(user=user, author=obj.id).exists()
        return False


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='author.email',
        required=False
    )
    id = serializers.IntegerField(
        source='author.id',
        required=False
    )
    username = serializers.CharField(
        source='author.username',
        required=False
    )
    first_name = serializers.CharField(
        source='author.first_name',
        required=False
    )
    last_name = serializers.CharField(
        source='author.last_name',
        required=False
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)

    def get_is_subscribed(self, obj):
        return (
            Follow.objects.filter(
                user=obj.user,
                author=obj.author
            ).exists()
        )

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_list_limit = None

        if 'recipes_limit' in request.query_params:
            recipes_list_limit = int(
                request.query_params.get('recipes_limit')
            )

        queryset = Recipe.objects.filter(
            author=obj.author
        )[:recipes_list_limit]

        serializer = RecipeReadSerializer(queryset,
                                          many=True,)

        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class RecipeReadSerializer(serializers.ModelSerializer):
    author = FoodUserSerializer(
        read_only=True,
    )
    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='recipe_ingredient',
        read_only=True
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                #   'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = None
        request = self.context.get('request')

        if request and hasattr(request, 'user'):
            user = request.user
        if user and user.is_authenticated:
            return obj.favourite.filter(user=user).exists()

        return False

    # def get_is_in_shopping_cart(self, obj):
    #     user = self.context.get('request').user
    #     if user and user.is_authenticated:
    #         return obj.basket_recipes.filter(user=user).exists()
    #     return False


class RecipeWriteOrUpdateSerializer(serializers.ModelSerializer):
    author = FoodUserSerializer(
        read_only=True,
    )
    ingredients = serializers.ListField(
        child=serializers.DictField(),
    )
    tags = serializers.ListField(
        child=serializers.SlugRelatedField(
            slug_field='id',
            queryset=Tag.objects.all(),
        ),
    )
    image = Base64ImageField(
        max_length=None,
        use_url=True
    )

    class Meta:
        model = Recipe
        fields = ('ingredients',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time',
                  'author',)

    def validate(self, data):
        ingredient_list = [
            ingredient.get('id') for ingredient in data.get('ingredients')
        ]           
        if len(ingredient_list) != len(set(ingredient_list)):
            raise serializers.ValidationError(
                'Повторное указание ингредиента!'
            )
        return data

    def get_ingredients_and_tags(self, validated_data):
        try:
            return (
                validated_data.pop('ingredients'),
                validated_data.pop('tags')
            )
        except KeyError:
            raise serializers.ValidationError('Не указаны ингридиенты или тэги')

    def set_ingredients_and_tags(self, recipe, ingredients, tags):
        ingredients_insert = [
            IngredientRecipe(
                ingredient=get_object_or_404(Ingredient, id=ingredient.get('id')),
                recipe=recipe,
                amount=ingredient.get('amount')
            ) for ingredient in ingredients
        ]
        IngredientRecipe.objects.bulk_create(ingredients_insert)

        recipe.tags.set(tags)
        return recipe

    def create(self, validated_data):
        ingredients, tags = self.get_ingredients_and_tags(validated_data)
        recipe = Recipe.objects.create(**validated_data)
        return self.set_ingredients_and_tags(recipe, ingredients, tags)

    def update(self, instance, validated_data):
        instance.ingredients.clear()
        instance.tags.clear()

        ingredients, tags = self.get_ingredients_and_tags(validated_data)
        instance = self.set_ingredients_and_tags(
            instance,
            ingredients,
            tags,
        )
        return super().update(instance, validated_data)


class FavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavouriteRecipe
        fields = ('user', 'recipe')

    def validate(self, data):
        user = self.context['request'].user
        recipe_id = self.context.get('view').kwargs.get('recipe_id')

        if FavouriteRecipe.objects.filter(
            user=user.id,
            recipe=recipe_id
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже в избранном!')
        return data