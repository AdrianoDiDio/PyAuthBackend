from django.shortcuts import render
from PyAuthBackend.AuthRESTAPI.models import User
from PyAuthBackend.AuthRESTAPI.serializers import UserSerializer
from PyAuthBackend.AuthRESTAPI.tokens import generateBiometricToken
from rest_framework import viewsets,permissions,mixins,status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

@method_decorator(
    name='create',
    decorator=swagger_auto_schema(
        operation_description="Register a new user by providing an Username/Email/Password.",
        responses={
            400: 'if one of the parameters was not set or was not valid.',
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'Id': Schema(
                        type=TYPE_NUMBER
                    ),
                    'Username': Schema(
                        type=TYPE_STRING
                    ),
                    'Email': Schema(
                        type=TYPE_STRING
                    )
                }
            )
        },
))
class RegisterUserView(mixins.CreateModelMixin,viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = Response()
        user = User.objects.filter(id=serializer.data.get('id')).first()
        #token = Token.objects.create(user=user)
        response.data = {
                'user' : serializer.data
                #'bioToken' : token.key
        }
        response.status=status.HTTP_201_CREATED
        response.headers=headers
        return response




