from django.contrib import admin

from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import (Category, Product, ProductSpecification,
                     ProductSpecificationValue, ProductType, ProductImages,Comments)
admin.site.register(Category, MPTTModelAdmin)
"""class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20

    list_display=(
        'tree_actions',
        'indented_title',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    )"""
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 3
    
@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline,]
    
class ProductImageInline(admin.TabularInline):
    model = ProductImages
    extra = 4
    
class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue
    extra = 5
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline, 
        ProductImageInline,
    ]
    """
    list_display = ['title', 'description', 'created_at']
    list_filter = ['title', 'created_at']
    list_editable = ['description']
    """
    prepopulated_fields = {'slug':('title',)}

@admin.register(Comments)
class Comments(admin.ModelAdmin):
    pass
