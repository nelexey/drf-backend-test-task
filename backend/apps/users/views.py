from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, AuthToken
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, UserUpdateSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            from apps.access_control.models import Role, UserRole
            default_role = Role.objects.filter(name='user').first()
            if default_role:
                UserRole.objects.create(user=user, role=default_role)
            return Response({'message': 'Регистрация успешна'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not user.is_active:
                return Response({'error': 'Аккаунт деактивирован'}, status=status.HTTP_401_UNAUTHORIZED)
            
            if not user.check_password(password):
                return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
            
            token = AuthToken.objects.create(
                user=user,
                token=AuthToken.generate_token(),
                expires_at=timezone.now() + timedelta(days=1)
            )
            
            response = Response({
                'token': token.token,
                'user': UserSerializer(user).data
            })
            response.set_cookie('auth_token', token.token, httponly=True, max_age=86400)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.auth:
            request.auth.delete()
        response = Response({'message': 'Выход выполнен'})
        response.delete_cookie('auth_token')
        return response


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        if request.auth:
            request.auth.delete()
        response = Response({'message': 'Аккаунт деактивирован'})
        response.delete_cookie('auth_token')
        return response
