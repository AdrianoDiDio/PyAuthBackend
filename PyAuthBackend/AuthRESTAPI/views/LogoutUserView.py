from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import permissions,status

class LogoutUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        try:
            refreshToken = request.data["refresh"]
            token = RefreshToken(refreshToken)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
