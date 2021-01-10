from django.shortcuts import render
from PyAuthBackend.AuthRESTAPI.models import User
from PyAuthBackend.AuthRESTAPI.serializers import UserPublicKeySerializer,UserAuthTokenSerializer
from PyAuthBackend.AuthRESTAPI.tokens import generateBiometricToken
from PyAuthBackend.AuthRESTAPI.exceptions import InvalidRSASignature,InvalidBiometricChallenge
from rest_framework import viewsets,permissions,mixins,status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from drf_yasg.openapi import Schema,TYPE_OBJECT,TYPE_STRING,TYPE_NUMBER
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics,exceptions
from rest_framework.views import APIView
import base64
import secrets
import uuid
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1,SHA256
from Crypto.Signature import pss

PublicKey = openapi.Parameter('publicKey', openapi.IN_QUERY, description="Public Key used to encrypt the biometric token encoded using Base64",
                              type=openapi.TYPE_STRING)

@method_decorator(
    name='get',
    decorator=swagger_auto_schema(
        operation_description="Generate a new biometric token for the user using the Public Key.",
        responses={
            400: 'if user has not provided a public key.',
            200: Schema(
                type=TYPE_OBJECT,
                properties={
                    'biometricToken': Schema(
                        type=TYPE_STRING
                    ),
                }
            )
        }
))

class GetBiometricChallenge(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserPublicKeySerializer

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def get(self,request):
        try:
            userInstance = self.get_object()
            challenge = str(uuid.uuid4())
            encodedChallenge = base64.urlsafe_b64encode(challenge.encode()).decode('UTF-8')
            encodedchallengeJSON = {"biometricChallenge" : encodedChallenge}
            #serializer = UserPublicKeySerializer(userInstance,data=request.data)
            #serializer.is_valid(raise_exception=True)
            #serializer.save()
            return Response(encodedchallengeJSON,status=status.HTTP_200_OK)
        except exceptions.ValidationError as v:
            raise v

class GenerateBiometricTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserAuthTokenSerializer

    def get_object(self):
        return User.objects.get(username=self.request.user)

    def post(self,request):
        try:
            userInstance = self.get_object()
            #publicKeyObject = RSA.importKey(base64.urlsafe_b64decode(userInstance.publicKey))
            publicKeyObject = RSA.importKey(base64.urlsafe_b64decode(request.data['publicKey']))
            originalEncodedChallenge = base64.urlsafe_b64decode(request.data['serverBiometricChallenge']).decode("UTF-8")
            originalChallenge = originalEncodedChallenge + request.data['nonce']
            sentChallenge = base64.urlsafe_b64decode(request.data['signedBiometricChallenge'])
            verifierRSA = pkcs1_15.new(publicKeyObject)
            digest = SHA256.new()
            digest.update(originalChallenge.encode())
            verifierRSA.verify(digest,sentChallenge)
            authBiometricToken = secrets.token_bytes(32)
            encodedAuthBiometricToken = base64.urlsafe_b64encode(authBiometricToken).decode('ascii')
            authBiometricTokenJSon = {"biometricToken" : encodedAuthBiometricToken}
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data.update(authBiometricTokenJSon)
            request.data._mutable = _mutable
            serializer = UserAuthTokenSerializer(userInstance,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            cipherRSA = PKCS1_OAEP.new(publicKeyObject,hashAlgo=SHA256,mgfunc=lambda x,y: pss.MGF1(x,y,SHA1))
            outAuthBiometricToken = base64.urlsafe_b64encode(cipherRSA.encrypt(authBiometricToken))
            userId = str(userInstance.id)
            outAuthBiometricTokenJSon = {"userId" : userId,"biometricToken" :  outAuthBiometricToken}
            request.session.flush()
            return Response(outAuthBiometricTokenJSon,status=status.HTTP_201_CREATED)
        except (ValueError,TypeError) as vte:
            raise InvalidRSASignature
        except exceptions.ValidationError as v:
            raise v





