from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST)

from core.models import BasketUser
from core.utils import get_shopping_list_pdf
from recipes.models import (FavouriteRecipe, Follow, Ingredient,
                            IngredientRecipe, Recipe, Tag)

from .filters import RecipeFilter
from .permissions import AuthorOrReadOnly
from .serializers import (FoodUserSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteOrUpdateSerializer,
                          SubscribeSerializer, TagSerializer)

User = get_user_model()


class RecipeViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (
        AuthorOrReadOnly,
    )
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeWriteOrUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer = RecipeReadSerializer(
            instance=serializer.instance,
            context={'request': self.request}
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        serializer = RecipeReadSerializer(
            instance=serializer.instance,
            context={'request': self.request},
        )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=HTTP_200_OK, headers=headers
        )

    def add_recipe(self, request, model, id=None):
        user = request.user

        if model.objects.filter(
            user=user,
            recipe__id=id
        ).exists():
            return Response({
                'errors': 'Рецепт уже добавлен в избранное!'},
                status=HTTP_400_BAD_REQUEST
            )

        recipe = get_object_or_404(Recipe, id=id)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeReadSerializer(recipe)

        return Response(serializer.data, status=HTTP_201_CREATED)

    def del_recipe(self, request, model, id=None):
        user = request.user
        favorite_recipe = model.objects.filter(
            user=user,
            recipe__id=id
        )

        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Удаление несуществующего рецепта невозможно!'},
            status=HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='favorite',
        url_name='favorite',
    )
    def add_or_del_favorite(self, request, pk=None):
        if request.method == 'POST':
            return self.add_recipe(request, FavouriteRecipe, pk)
        if request.method == 'DELETE':
            return self.del_recipe(request, FavouriteRecipe, pk)
        return None

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='shopping_cart',
        url_name='shopping_cart',
    )
    def shopping_cart(self, request, pk=None):
        if request.method == 'DELETE':
            return self.del_recipe(request, BasketUser, pk)
        if request.method == 'POST':
            return self.add_recipe(request, BasketUser, pk)
        return None

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,),
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        user = request.user

        if not user.basket.exists():
            return Response(
                {'errors': 'Список покупок пустой!'},
                status=HTTP_400_BAD_REQUEST
            )

        basket_ingredients = IngredientRecipe.objects.filter(
            recipe__basket_recipe__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by('ingredient__name')

        return get_shopping_list_pdf(basket_ingredients)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = IngredientSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        name = self.request.query_params.get('name')
        if name is not None:
            return queryset.filter(name__iregex=f'^{name}')
        return queryset


class SpecialUserViewSet(UserViewSet):
    queryset = User.objects.all().prefetch_related('recipes')
    serializer_class = FoodUserSerializer
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]'

    http_method_names = ('get', 'post', 'delete')

    def add_subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)

        if user == author:
            return Response(
                {'errors': 'Подписка на себя запрещена!'},
                status=HTTP_400_BAD_REQUEST
            )

        follow, status = Follow.objects.get_or_create(user=user, author=author)

        if status:
            serializer = SubscribeSerializer(
                follow, context={'request': request}
            )
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(
            {'errors': 'Повторная попытка подписки!'},
            status=HTTP_400_BAD_REQUEST
        )

    def del_subscribe(self, request, pk=None):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        followers = get_object_or_404(Follow, user=user, author=author)
        followers.delete()

        return Response(status=HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscribeSerializer,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def get_subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='subscribe',
        url_name='subscribe',
    )
    def add_or_del_subscribe(self, request, pk=None):
        if request.method == 'POST':
            return self.add_subscribe(request, pk)
        if request.method == 'DELETE':
            return self.del_subscribe(request, pk)
        return None
