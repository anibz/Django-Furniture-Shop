from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
import uuid

User = get_user_model()


class Order(models.Model):
    """შეკვეთების მოდელი"""
    STATUS_CHOICES = [
        ('pending', 'მიმდინარე'),
        ('processing', 'მუშავდება'),
        ('shipped', 'გაგზავნილი'),
        ('delivered', 'მიტანილი'),
        ('cancelled', 'გაუქმებული'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='მომხმარებელი')
    order_number = models.CharField(max_length=50, unique=True, verbose_name='შეკვეთის ნომერი')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='სტატუსი')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ჯამური თანხა')
    shipping_address = models.TextField(verbose_name='მიწოდების მისამართი')
    phone = models.CharField(max_length=20, verbose_name='ტელეფონი')
    notes = models.TextField(blank=True, null=True, verbose_name='შენიშვნები')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='შექმნის თარიღი')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='განახლების თარიღი')

    class Meta:
        verbose_name = 'შეკვეთა'
        verbose_name_plural = 'შეკვეთები'
        ordering = ['-created_at']

    def __str__(self):
        return f"შეკვეთა #{self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """შეკვეთაში არსებული ცალკეული პროდუქტი"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='შეკვეთა')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='პროდუქტი')
    quantity = models.PositiveIntegerField(verbose_name='რაოდენობა')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ფასი შეკვეთის დროს')

    class Meta:
        verbose_name = 'შეკვეთის პროდუქტი'
        verbose_name_plural = 'შეკვეთის პროდუქტები'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def get_total_price(self):
        """ამ პროდუქტის ჯამური ფასი"""
        return self.price * self.quantity