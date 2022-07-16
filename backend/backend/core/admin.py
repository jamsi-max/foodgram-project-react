from django.contrib import admin

from .models import BasketUser


class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes_count')
    list_filter = ('user', )
    search_fields = ('user__username',)
    ordering = ('user',)


admin.site.register(BasketUser, BasketAdmin)
