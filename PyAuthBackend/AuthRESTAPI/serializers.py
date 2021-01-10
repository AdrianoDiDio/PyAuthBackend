from rest_framework import serializers,exceptions as rest_exceptions
from rest_framework.validators import UniqueValidator
from PyAuthBackend.AuthRESTAPI.models import User
from django.core import exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainSerializer,TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import default_user_authentication_rule
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext as _
import base64

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={'placeholder': 'Email'},
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={'placeholder': 'Username'},
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        errors = dict() 
        try:
            validators.validate_password(password=password, user=username)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(UserSerializer, self).validate(data)
    
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],validated_data['password'])
        return user
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        
class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        style={'placeholder': 'Username'},
    )
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password', 'placeholder': 'Password'},
        min_length=8
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        
class UserAuthTokenSerializer(serializers.ModelSerializer):
    biometricToken = serializers.CharField(
        required = True,
        write_only = True
    )
    def update(self,instance,validated_data):
        decodedBiometricToken = base64.urlsafe_b64decode(validated_data.get('biometricToken'))
        instance.biometricToken = make_password(decodedBiometricToken)
        instance.save()
        return instance
    class Meta:
        model = User
        fields = ('biometricToken',)

class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        read_only=True
    )
    username = serializers.CharField(
        read_only=True
    )
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class BiometricTokenObtainSerializer(TokenObtainSerializer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password'].required = False
        self.fields['userId'] = serializers.CharField()
        self.fields['biometricToken'] = serializers.CharField()
    
    def validate(self,attr):
        #biometricToken = base64.urlsafe_b64decode(attr['biometricToken'])
        authenticate_kwargs = {
            'userId' : attr['userId'],
            'biometricToken' : attr['biometricToken'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not default_user_authentication_rule(self.user):
            raise rest_exceptions.AuthenticationFailed(
                _('Given Biometric Token was not valid.'),
                'invalid_biometric_token',
            )
        return {}
class BiometricTokenObtainPairSerializer(BiometricTokenObtainSerializer):

    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        update_last_login(None, self.user)

        return data    
