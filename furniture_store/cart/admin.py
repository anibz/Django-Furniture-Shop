from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """კალათის პროდუქტების Inline"""
    model = CartItem
    extra = 0
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """კალათების Admin პანელი"""
    list_display = ['user', 'get_total_items_count', 'get_total_price', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'updated_at']
    inlines = [CartItemInline]

    def get_total_items_count(self, obj):
        return obj.get_total_items_count()

    get_total_items_count.short_description = 'პროდუქტების რაოდენობა'

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₾"

    get_total_price.short_description = 'ჯამური ფასი'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """კალათის პროდუქტების Admin"""
    list_display = ['cart', 'product', 'quantity', 'get_total_price']
    list_filter = ['cart__user']
    search_fields = ['product__name', 'cart__user__username']

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₾"

    get_total_price.short_description = 'ჯამი'