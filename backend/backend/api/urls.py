from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, SpecialUserViewSet,
                    TagViewSet)


router = DefaultRouter()
router.register("recipes", RecipeViewSet, basename="recipes")
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register('users', SpecialUserViewSet, basename='users')


urlpatterns = [
    path("", include(router.urls)),
]