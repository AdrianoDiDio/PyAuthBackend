from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
import base64

class BiometricTokenAuthBackend(ModelBackend):
    
    def get_user(self, user_id):
        try:
            User = get_user_model()
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
    def authenticate(self,request,userId=None,biometricToken=None):
        if userId is None:
            userId = request.data.get("userId","")
        if biometricToken is None :
            biometricToken = request.data.get("biometricToken","")
        if userId is None or biometricToken is None:
            return
        try:
            User = get_user_model()
            userToCheck = User.objects.get(id=userId)
        except User.DoesNotExist:
            return None
        decodedBiometricToken = base64.urlsafe_b64decode(biometricToken)
        if check_password(decodedBiometricToken,userToCheck.biometricToken):
            return userToCheck
        return None
