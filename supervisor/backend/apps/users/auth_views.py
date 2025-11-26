"""
Vues d'authentification JWT - SUPERVISOR V2.0

Ce module définit les vues d'authentification personnalisées avec JWT :
- Login : Authentification et obtention de tokens
- Register : Inscription d'un nouvel utilisateur
- Logout : Déconnexion avec blacklist du refresh token
- Refresh : Rafraîchissement du token d'accès
"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import UserCreateSerializer, UserProfileSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personnalisé pour inclure des informations supplémentaires dans le token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Ajouter des informations personnalisées dans le token
        token['username'] = user.username
        token['email'] = user.email

        # Ajouter des informations du profil si disponible
        if hasattr(user, 'profile'):
            token['code'] = user.profile.code
            token['nom'] = user.profile.nom
            token['prenoms'] = user.profile.prenoms
            token['role'] = user.profile.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Ajouter les informations complètes de l'utilisateur dans la réponse
        user_serializer = UserProfileSerializer(self.user)
        data['user'] = user_serializer.data

        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée pour l'obtention du token JWT avec informations utilisateur.
    """
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Authentification d'un utilisateur et obtention des tokens JWT.

    POST /api/auth/login/
    {
        "username": "user123",
        "password": "SecurePass123!"
    }

    Response:
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "profile": {
                "code": "AIV001",
                "nom": "KOUASSI",
                "prenoms": "Yao",
                "role": "SUPERVISEUR",
                ...
            }
        }
    }
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Le nom d\'utilisateur et le mot de passe sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Authentifier l'utilisateur
    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {'error': 'Identifiants invalides'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {'error': 'Ce compte est désactivé'},
            status=status.HTTP_403_FORBIDDEN
        )

    # Générer les tokens JWT
    refresh = RefreshToken.for_user(user)

    # Ajouter des informations personnalisées dans le token
    refresh['username'] = user.username
    refresh['email'] = user.email

    if hasattr(user, 'profile'):
        refresh['code'] = user.profile.code
        refresh['nom'] = user.profile.nom
        refresh['prenoms'] = user.profile.prenoms
        refresh['role'] = user.profile.role

    # Retourner les tokens avec les informations de l'utilisateur
    user_serializer = UserProfileSerializer(user)

    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Inscription d'un nouvel utilisateur.

    POST /api/auth/register/
    {
        "username": "user123",
        "email": "user@example.com",
        "password": "SecurePass123!",
        "password2": "SecurePass123!",
        "code": "AIV001",
        "nom": "KOUASSI",
        "prenoms": "Yao",
        "telephone": "+225XXXXXXXXXX",
        "role": "SUPERVISEUR"
    }

    Response:
    {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "profile": {
                "code": "AIV001",
                "nom": "KOUASSI",
                "prenoms": "Yao",
                "role": "SUPERVISEUR",
                ...
            }
        }
    }
    """
    serializer = UserCreateSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        # Générer les tokens JWT pour l'utilisateur nouvellement créé
        refresh = RefreshToken.for_user(user)

        # Ajouter des informations personnalisées dans le token
        refresh['username'] = user.username
        refresh['email'] = user.email

        if hasattr(user, 'profile'):
            refresh['code'] = user.profile.code
            refresh['nom'] = user.profile.nom
            refresh['prenoms'] = user.profile.prenoms
            refresh['role'] = user.profile.role

        # Retourner les tokens avec les informations de l'utilisateur
        user_serializer = UserProfileSerializer(user)

        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Déconnexion d'un utilisateur avec blacklist du refresh token.

    POST /api/auth/logout/
    {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }

    Le refresh token est ajouté à la blacklist pour empêcher son utilisation future.
    L'access token continue de fonctionner jusqu'à son expiration (2h par défaut).
    """
    try:
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {'error': 'Le refresh token est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Ajouter le refresh token à la blacklist
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {'detail': 'Déconnexion réussie'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {'error': f'Erreur lors de la déconnexion : {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_token_view(request):
    """
    Vérifie que le token d'accès est valide.

    POST /api/auth/verify/
    Authorization: Bearer {access_token}

    Response:
    {
        "detail": "Token valide",
        "user": {
            "id": 1,
            "username": "user123",
            "email": "user@example.com",
            "profile": {
                ...
            }
        }
    }
    """
    user_serializer = UserProfileSerializer(request.user)

    return Response({
        'detail': 'Token valide',
        'user': user_serializer.data
    }, status=status.HTTP_200_OK)
