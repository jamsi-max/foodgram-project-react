from django.contrib import admin

from .models import (FavouriteRecipe, Follow, Ingredient, IngredientRecipe,
                     Recipe, Tag)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'in_favourite_count', 'pub_date',)
    inlines = (IngredientRecipeInline,)
    search_fields = ('name', 'author__username', 'tags__name',)
    list_filter = ('author', 'name', 'tags',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)
    search_fields = ('ingredient', 'recipe',)
    list_filter = ('ingredient', 'recipe',)


class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'recipes_count')
    search_fields = ('recipe',)
    list_filter = ('user', 'recipe',)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('author', 'folower_count', 'folowing_count')
    search_fields = ('user', 'author',)
    list_filter = ('user', 'author',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(FavouriteRecipe, FavouriteRecipeAdmin)
admin.site.register(Follow, FollowAdmin)
