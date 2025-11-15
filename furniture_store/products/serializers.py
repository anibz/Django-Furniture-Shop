from rest_framework import serializers
from .models import Category, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    """კატეგორიების Serializer"""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    """პროდუქტის სურათების Serializer"""

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main']


class ProductSerializer(serializers.ModelSerializer):
    """პროდუქტების დეტალური Serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'description', 'price', 'stock', 'is_available',
            'featured', 'color', 'material', 'images',
            'created_at', 'updated_at'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    """პროდუქტების სიის Serializer (გამარტივებული)"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category_name',
            'price', 'stock', 'is_available',
            'featured', 'color', 'material', 'main_image'
        ]

    def get_main_image(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        if main_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main_image.image.url)
        return None