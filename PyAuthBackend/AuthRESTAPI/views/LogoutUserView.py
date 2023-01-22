from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import permissions,status
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Blacklist the refresh token making it impossible to refresh the access token when expired.",
        responses={
            400: 'if refresh token is not valid or it is already blacklisted.',
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'access': Schema(
                        type=TYPE_STRING
                    ),
                }
            )
        },
        request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                required=['refresh'],
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING)
                },
        ),
    )
)

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

