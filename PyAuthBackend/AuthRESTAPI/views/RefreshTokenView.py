from django.shortcuts import render
from PyAuthBackend.AuthRESTAPI.models import User
from PyAuthBackend.AuthRESTAPI.serializers import UserAuthTokenSerializer
from PyAuthBackend.AuthRESTAPI.tokens import generateBiometricToken
from rest_framework import viewsets,permissions,mixins,status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

@method_decorator(
    name='create', 
    decorator=swagger_auto_schema(
        operation_description="Refresh an user authentication token by using a refresh token.",
        responses={
            400: 'if refresh token was not valid or expired.',
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'AuthToken': Schema(
                        type=TYPE_STRING
                    )
                }
            )
        },
))
class RefreshTokenView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserAuthTokenSerializer
        
    @method_decorator(ensure_csrf_cookie)
    def create(self,request):
        User = get_user_model()
        refreshToken = request.COOKIES.get('RefreshToken')
        if refreshToken is None:
            raise exceptions.AuthenticationFailed('Authentication credentials were not provided.')
        try:
            payload = jwt.decode(refreshToken, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('expired refresh token, please login again.')
        user = User.objects.filter(id=payload.get('userID')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
        accessToken = generateAccessToken(user)
        return Response({'AccessToken': access_token})
        
    

 
 
