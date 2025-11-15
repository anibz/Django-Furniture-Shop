from django.shortcuts import render

# Create your views here.

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import UserRegistrationSerializer, UserSerializer, PasswordChangeSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    POST /api/register/ - მომხმარებლის რეგისტრაცია
    """
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Token-ის შექმნა
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'რეგისტრაცია წარმატებით დასრულდა'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    POST /api/login/ - მომხმარებლის ავტორიზაცია
    Body: {"username": "user", "password": "pass"}
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'გთხოვთ შეავსოთ username და password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'ავტორიზაცია წარმატებით დასრულდა'
        })
    else:
        return Response(
            {'error': 'არასწორი username ან password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    GET /api/profile/ - ავტორიზებული მომხმარებლის პროფილი
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def user_profile_update(request):
    """
    PUT /api/profile/update/ - პროფილის განახლება
    """
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'user': serializer.data,
            'message': 'პროფილი წარმატებით განახლდა'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    POST /api/change-password/ - პაროლის ცვლილება
    Body: {
        "old_password": "old",
        "new_password": "new",
        "new_password2": "new"
    }
    """
    serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'პაროლი წარმატებით შეიცვალა'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)