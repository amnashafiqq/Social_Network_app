from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from authentication.serializers import UserSerializer, TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from authentication.serializers import PostSerializer



class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class TokenObtainPairView(generics.CreateAPIView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]
    
@api_view(['POST'])
def signup(request):
    User = get_user_model()
    email = request.data.get('email')
    password = request.data.get('password')

    # Validate email format
    try:
        User._meta.get_field('email').clean(email, User())
    except ValidationError as e:
        return JsonResponse({'error': 'Invalid email format'}, status=400)

    # Create new user
    user = User.objects.create_user(email=email, password=password)

    # Enrich user with geolocation data asynchronously
    # Assuming you have set up Celery for background task processing
    # You can replace the following code with your specific background task implementation
    # Make sure to install and configure Celery and a message broker like RabbitMQ or Redis
    enrich_user_geolocation.delay(user.id)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({'access_token': access_token})

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, username=email, password=password)

    # Check if authentication was successful
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

    # Generate JWT tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    return JsonResponse({'access_token': access_token})

