from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    biometricToken = models.CharField(max_length=256,null=True,default=None)
    publicKey = models.CharField(max_length=2048,null=True,default=None)
