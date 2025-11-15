from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import Cart


class OrderItemSerializer(serializers.ModelSerializer):
    """შეკვეთის პროდუქტების Serializer"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class OrderSerializer(serializers.ModelSerializer):
    """შეკვეთების Serializer"""
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_name',
            'status', 'total_amount', 'shipping_address',
            'phone', 'notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """შეკვეთის შექმნის Serializer"""

    class Meta:
        model = Order
        fields = ['shipping_address', 'phone', 'notes']

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)

        # შეკვეთის შექმნა
        order = Order.objects.create(
            user=user,
            total_amount=cart.get_total_price(),
            **validated_data
        )

        # კალათიდან პროდუქტების გადატანა შეკვეთაში
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

            # მარაგის განახლება
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()

        # კალათის გასუფთავება
        cart.items.all().delete()

        return order