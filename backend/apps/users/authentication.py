from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import AuthToken


class SessionTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            token = request.COOKIES.get('auth_token')
        
        if not token:
            return None
        
        if token.startswith('Token '):
            token = token[6:]
        
        try:
            auth_token = AuthToken.objects.select_related('user').get(
                token=token,
                expires_at__gt=timezone.now()
            )
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed('Недействительный или истекший токен')
        
        if not auth_token.user.is_active:
            raise AuthenticationFailed('Аккаунт деактивирован')
        
        return (auth_token.user, auth_token)
