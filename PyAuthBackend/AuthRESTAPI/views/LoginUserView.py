from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from PyAuthBackend.AuthRESTAPI.serializers import BiometricTokenObtainPairSerializer
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Log-In the User using Username/Password.\nReturns a Refresh and an Authentication Token.",
        responses={
            400: 'if user does not exists or any of the required field was not valid.',
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
        }
))

class LoginTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        operation_description="Log-In the User using userId/biometricToken.\nReturns a Refresh and an Authentication Token.",
        responses={
            400: 'if user does not exists or any of the required field was not valid.',
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
        }
))
class BiometricLoginTokenObtainPairView(jwt_views.TokenObtainPairView):
    serializer_class = BiometricTokenObtainPairSerializer
