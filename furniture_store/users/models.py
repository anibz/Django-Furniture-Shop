from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    მორგებული მომხმარებლის მოდელი დამატებითი ველებით
    """
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='ტელეფონი')
    address = models.TextField(blank=True, null=True, verbose_name='მისამართი')
    birth_date = models.DateField(blank=True, null=True, verbose_name='დაბადების თარიღი')

    class Meta:
        verbose_name = 'მომხმარებელი'
        verbose_name_plural = 'მომხმარებლები'

    def get_full_name(self):
        """აბრუნებს სრულ სახელს"""
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def __str__(self):
        return self.get_full_name()