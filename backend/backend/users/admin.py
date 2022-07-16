from django.contrib import admin

from .models import FoodUser


class FoodUserAdmin(admin.ModelAdmin):
    list_display = ('email','username', 'folower_count', 'folowing_count',)
    list_filter = ('username', )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(FoodUser, FoodUserAdmin)
