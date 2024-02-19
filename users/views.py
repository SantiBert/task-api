from rest_framework import generics,permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LogOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Check if the Authorization header exists
            if 'Authorization' in request.headers:
                # Extract the token from the Authorization header
                auth_header = request.headers['Authorization']
                token_type, token_value = auth_header.split()
                # Check if the token type is 'Bearer'
                if token_type == 'Bearer':
                    # Use the RefreshToken class to blacklist the refresh token
                    token = RefreshToken(token_value)
                    token.blacklist()
                    return Response({"message": "LogOut"}, status=status.HTTP_205_RESET_CONTENT)
                else:
                    # If the token type is not 'Bearer', return a 400 Bad Request response
                    return Response({"error": "Invalid token type"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If the Authorization header is missing, return a 400 Bad Request response
                return Response({"error": "Authorization header missing"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any other exceptions and return a 400 Bad Request response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        # El token de acceso ha sido validado correctamente
        return Response({"message": "Token valid"}, status=status.HTTP_200_OK)