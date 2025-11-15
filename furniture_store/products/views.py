from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    კატეგორიების ViewSet (მხოლოდ წაკითხვა)
    GET /api/categories/ - ყველა კატეგორია
    GET /api/categories/{slug}/ - კონკრეტული კატეგორია
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    პროდუქტების ViewSet (მხოლოდ წაკითხვა)
    GET /api/products/ - ყველა პროდუქტი
    GET /api/products/{slug}/ - კონკრეტული პროდუქტი
    ფილტრაცია: ?category=1&color=black&material=wood
    """
    queryset = Product.objects.filter(is_available=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'color', 'material', 'featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer