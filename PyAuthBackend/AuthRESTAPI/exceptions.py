from rest_framework.exceptions import APIException
from django.utils.translation import gettext as _

class InvalidRSASignature(APIException):
    status_code = 400
    default_detail = _('Invalid signature detected')
    default_code = 'invalid_signature'
    
class InvalidBiometricChallenge(APIException):
    status_code = 400
    default_detail = _('Invalid biometric challenge detected')
    default_code = 'invalid_biometric_challenge'
