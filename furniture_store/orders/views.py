from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Order
from cart.models import Cart
from .serializers import OrderSerializer, OrderCreateSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    შეკვეთების ViewSet
    GET /api/orders/ - ყველა შეკვეთა (auth user)
    GET /api/orders/{id}/ - კონკრეტული შეკვეთა
    POST /api/orders/create_order/ - ახალი შეკვეთის შექმნა
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # მომხმარებელი ხედავს მხოლოდ საკუთარ შეკვეთებს
        return Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create_order':
            return OrderCreateSerializer
        return OrderSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        """
        POST /api/orders/create_order/ - ახალი შეკვეთის შექმნა
        Body: {
            "shipping_address": "მისამართი",
            "phone": "555123456",
            "notes": "შენიშვნები (optional)"
        }
        """
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                order = serializer.save()
                order_serializer = OrderSerializer(order)
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
            except Cart.DoesNotExist:
                return Response(
                    {'error': 'კალათა ცარიელია'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)