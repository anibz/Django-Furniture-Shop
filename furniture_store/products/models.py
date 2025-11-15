from django.db import models

# Create your models here.


from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """პროდუქტების კატეგორიები"""
    name = models.CharField(max_length=200, verbose_name='სახელი')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='აღწერა')
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name='სურათი')
    is_active = models.BooleanField(default=True, verbose_name='აქტიური')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='შექმნის თარიღი')

    class Meta:
        verbose_name = 'კატეგორია'
        verbose_name_plural = 'კატეგორიები'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """პროდუქტების მოდელი"""
    COLOR_CHOICES = [
        ('white', 'თეთრი'),
        ('black', 'შავი'),
        ('brown', 'ყავისფერი'),
        ('gray', 'ნაცრისფერი'),
        ('beige', 'ბეჟი'),
        ('red', 'წითელი'),
        ('blue', 'ლურჯი'),
        ('green', 'მწვანე'),
    ]

    MATERIAL_CHOICES = [
        ('wood', 'ხე'),
        ('metal', 'ლითონი'),
        ('glass', 'მინა'),
        ('leather', 'ტყავი'),
        ('textile', 'ტექსტილი'),
        ('plastic', 'პლასტიკი'),
    ]

    name = models.CharField(max_length=200, verbose_name='დასახელება')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='კატეგორია')
    description = models.TextField(verbose_name='აღწერა')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='ფასი')
    stock = models.IntegerField(default=0, verbose_name='მარაგი')
    is_available = models.BooleanField(default=True, verbose_name='ხელმისაწვდომი')
    featured = models.BooleanField(default=False, verbose_name='გამორჩეული')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, verbose_name='ფერი')
    material = models.CharField(max_length=20, choices=MATERIAL_CHOICES, verbose_name='მასალა')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='შექმნის თარიღი')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='განახლების თარიღი')

    class Meta:
        verbose_name = 'პროდუქტი'
        verbose_name_plural = 'პროდუქტები'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """პროდუქტის დამატებითი სურათები"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='პროდუქტი')
    image = models.ImageField(upload_to='products/', verbose_name='სურათი')
    is_main = models.BooleanField(default=False, verbose_name='მთავარი სურათი')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'პროდუქტის სურათი'
        verbose_name_plural = 'პროდუქტის სურათები'

    def __str__(self):
        return f"{self.product.name} - სურათი"