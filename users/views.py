from rest_framework import generics,permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer


class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.headers['Authorization'].split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "LogOut"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)},status=status.HTTP_400_BAD_REQUEST)