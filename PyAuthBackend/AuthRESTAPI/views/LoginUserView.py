from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from PyAuthBackend.AuthRESTAPI.serializers import BiometricTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

Username = openapi.Parameter('username', openapi.IN_QUERY, description="Username", 
                              type=openapi.TYPE_STRING)
Password = openapi.Parameter('password', openapi.IN_QUERY, description="Password", 
                              type=openapi.TYPE_STRING)
BiometricToken = openapi.Parameter('biometricToken', openapi.IN_QUERY, description="BiometricToken (Optional)", 
                              type=openapi.TYPE_STRING)
@method_decorator(
    name='post', 
    decorator=swagger_auto_schema(
        operation_description="Log-In the User using either Username/Password or the Biometric Token.\nReturns a Refresh and an Authentication Token.",
        responses={
            400: 'if user has not provided a public key.',
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'refresh': Schema(
                        type=TYPE_STRING
                    ),
                    'access': Schema(
                        type=TYPE_STRING
                    ),
                }
            )
        },
        manual_parameters=[
            Username,
            Password,
            BiometricToken
        ],
))
        
class LoginTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class BiometricLoginTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = BiometricTokenObtainPairSerializer
