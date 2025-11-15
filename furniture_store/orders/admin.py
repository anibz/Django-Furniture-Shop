from django.contrib import admin

# Register your models here.


from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """შეკვეთის პროდუქტების Inline"""
    model = OrderItem
    extra = 0
    fields = ['product', 'quantity', 'price']
    readonly_fields = ['product', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """შეკვეთების Admin პანელი"""
    list_display = ['order_number', 'user', 'status', 'total_amount', 'phone', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('შეკვეთის ინფორმაცია', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('მიწოდების ინფორმაცია', {
            'fields': ('shipping_address', 'phone', 'notes')
        }),
        ('თარიღები', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """შეკვეთის პროდუქტების Admin"""
    list_display = ['order', 'product', 'quantity', 'price', 'get_total_price']
    list_filter = ['order__status', 'order__created_at']
    search_fields = ['order__order_number', 'product__name']

    def get_total_price(self, obj):
        return f"{obj.get_total_price()} ₾"

    get_total_price.short_description = 'ჯამი'