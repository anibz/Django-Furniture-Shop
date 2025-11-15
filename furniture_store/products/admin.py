from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """პროდუქტის სურათების Inline"""
    model = ProductImage
    extra = 1
    fields = ['image', 'is_main']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """კატეგორიების Admin პანელი"""
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """პროდუქტების Admin პანელი"""
    list_display = ['name', 'category', 'price', 'stock', 'color', 'material', 'is_available', 'featured']
    list_filter = ['category', 'color', 'material', 'is_available', 'featured', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available', 'featured']
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """პროდუქტის სურათების Admin"""
    list_display = ['product', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name']