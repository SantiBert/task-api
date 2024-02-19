from rest_framework import generics,permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # El token de acceso ha sido validado correctamente
        return Response({"message": "Token valid"}, status=status.HTTP_200_OK)