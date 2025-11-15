from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product


class CartViewSet(viewsets.ViewSet):
    """
    კალათის ViewSet
    """
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        """
        GET /api/cart/{user_id}/ - მომხმარებლის კალათის ნახვა
        """
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        """
        POST /api/cart/add/ - პროდუქტის დამატება კალათაში
        Body: {"product_id": 1, "quantity": 2}
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response(
                {'error': 'product_id არის სავალდებულო'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            return Response(
                {'error': 'პროდუქტი ვერ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )

        # შევამოწმოთ მარაგი
        if product.stock < quantity:
            return Response(
                {'error': f'არასაკმარისი მარაგი. ხელმისაწვდომია: {product.stock}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # კალათის მიღება ან შექმნა
        cart, created = Cart.objects.get_or_create(user=request.user)

        # კალათის პროდუქტის მიღება ან შექმნა
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            # თუ პროდუქტი უკვე არის კალათაში, გავზარდოთ რაოდენობა
            new_quantity = cart_item.quantity + quantity
            if product.stock < new_quantity:
                return Response(
                    {'error': f'არასაკმარისი მარაგი. ხელმისაწვდომია: {product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartSerializer(cart, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        """
        POST /api/cart/remove/ - პროდუქტის წაშლა კალათიდან
        Body: {"product_id": 1}
        """
        product_id = request.data.get('product_id')

        if not product_id:
            return Response(
                {'error': 'product_id არის სავალდებულო'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()

            serializer = CartSerializer(cart, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'კალათა ვერ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'პროდუქტი კალათაში ვერ მოიძებნა'},
                status=status.HTTP_404_NOT_FOUND
            )