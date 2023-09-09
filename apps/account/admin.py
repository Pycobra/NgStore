from django.contrib import admin

from .models import UserBase


@admin.register(UserBase)
class ProductAdmin(admin.ModelAdmin):
    pass
    #list_display = ['name', 'created_at']
    #prepopulated_fields = {'slug':('name',)}


