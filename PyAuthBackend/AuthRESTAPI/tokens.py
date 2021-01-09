##import datetime
from datetime import datetime
from datetime import timedelta
import time
import jwt
from django.conf import settings
from rest_framework.authtoken.serializers import AuthTokenSerializer

'''
    Adriano:
    Biometric token is used to authenthicate users just by using FingerPrint or any other biometric auth method.
    This token has a long expiration date and it's supposed to be stored in a safe space on the user device,
    that can be used to simply auth the user without typing any login information.
    When a request is made and the token is expired frontend should request the user to login again in order to generate a new one.
'''
def generateBiometricToken(user):
    now = int(time.time())
    #Expire in 60 days
    expireInSeconds = 60 * 3600 * 24
    access_token_payload = {
        'userID': user.id,
        'Iat': now,
        'Exp': now + expireInSeconds,
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token

def generateAccessToken(user):
    now = int(time.time())
    #Expire in 5 minutes
    #expireInSeconds = 300
    expireInSeconds = 10
    access_token_payload = {
        'userID': user.id,
        'Iat': now,
        'Exp': now + expireInSeconds,
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token

def generateRefreshToken(user):
    now = int(time.time())
    #Expire in 2 days
    expireInSeconds = 2 * 3600 * 24
    access_token_payload = {
        'userID': user.id,
        'Iat': now,
        'Exp': now + expireInSeconds,
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token
