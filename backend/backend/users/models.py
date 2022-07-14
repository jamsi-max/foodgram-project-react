from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from .managers import FoodManager


class FoodUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            "Error": ("Email уже используется"),
        },
        verbose_name='Электронная почта',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                r"^[\w.@+-]+\Z",
                message="Username может содержать буквы, цифры и знак _",
            )
        ],
        verbose_name='Имя пользователя',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Персонал'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Время создания'
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    objects = FoodManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return self.username


#     class Meta:
#         constraints = (
#             models.UniqueConstraint(
#                 fields=['user', 'author'], name='unique_follow'
#             ),
#             # поля не могут ссылаться на один и тот же объект
            # models.CheckConstraint(
            #     check=~models.Q(user=models.F('author')),
            #     name='not_yourself_follow'
            # ),
#         )
#         ordering = ('author',)
#         verbose_name = 'Подписка пользователя'
#         verbose_name_plural = 'Подписки пользователей'

#     def __str__(self):
#         return (f'Подписчик {self.user.username[:15]}'
#                 f' на автора {self.author.username[:15]}')

#     # имена столбцов для админки logic
    # @property  # type: ignore
    # @admin.display(
    #     description='Имеет подписчиков',
    # )
    # def folower_count(self):
    #     """Сколько имеет подписчиков"""
    #     return self.user.following.count()

    # @property  # type: ignore
    # @admin.display(
    #     description='Подписан на',
    # )
    # def folowing_count(self):
    #     """На скольких пользователей подписан"""
    #     return self.user.follower.count()