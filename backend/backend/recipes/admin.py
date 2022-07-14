from django.contrib import admin

from .models import FavouriteRecipe, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    inlines = (IngredientRecipeInline,)
    search_fields = ('name', 'text')
    list_filter = ('author', 'name', 'tags')


class TagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('recipe',)
    list_filter = ('user', 'recipe')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(FavouriteRecipe, FavouriteRecipeAdmin)
