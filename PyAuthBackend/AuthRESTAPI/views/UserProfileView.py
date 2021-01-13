from django.shortcuts import render
from PyAuthBackend.AuthRESTAPI.models import User
from PyAuthBackend.AuthRESTAPI.serializers import UserProfileSerializer
from rest_framework import viewsets,permissions,mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema


@method_decorator(
    name='list',
    decorator=swagger_auto_schema(
        operation_description="Show the current logged in User.",
        responses={
            401: 'if user has not provided an authentication token or it is invalid.',
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
class UserProfileViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def list(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
