from django.contrib import admin

from .models import Vendor, Follow
from mptt.admin import MPTTModelAdmin

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'created_at']
    
admin.site.register(Follow)


