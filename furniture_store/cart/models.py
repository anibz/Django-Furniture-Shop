from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()


class Cart(models.Model):
    """მომხმარებლის კალათა"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='მომხმარებელი')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='განახლების თარიღი')

    class Meta:
        verbose_name = 'კალათა'
        verbose_name_plural = 'კალათები'

    def __str__(self):
        return f"{self.user.username}-ის კალათა"

    def get_total_price(self):
        """კალათის ჯამური ფასი"""
        total = sum(item.product.price * item.quantity for item in self.items.all())
        return total

    def get_total_items(self):
        """კალათაში არსებული პროდუქტების სია"""
        return self.items.all()

    def get_total_items_count(self):
        """კალათაში არსებული პროდუქტების რაოდენობა"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """კალათაში არსებული ცალკეული პროდუქტი"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='კალათა')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='პროდუქტი')
    quantity = models.PositiveIntegerField(default=1, verbose_name='რაოდენობა')

    class Meta:
        verbose_name = 'კალათის პროდუქტი'
        verbose_name_plural = 'კალათის პროდუქტები'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """ამ პროდუქტის ჯამური ფასი"""
        return self.product.price * self.quantity