from django.conf.urls import url
from django.urls import re_path,include
from rest_framework.routers import SimpleRouter
from PyAuthBackend.AuthRESTAPI.routers import WriteOnlyRouter
from rest_framework_simplejwt import views as jwt_views
from . import views

router = SimpleRouter(trailing_slash=False)
#writeOnlyRouter = WriteOnlyRouter(trailing_slash=False)
router.register(r'userDetails',views.UserProfileViewSet,basename="User Details")
router.register(r'register',views.RegisterUserView,basename="Register")
#router.register(r'getBiometricToken',views.GenerateBiometricTokenView,basename="GetBiometricToken")
#router.register(r'login',views.LoginUserView,basename="Login")
#writeOnlyRouter.register(r'token',jwt_views.TokenObtainPairView,basename="GenerateAuthToken")
#writeOnlyRouter.registry.extend(router.registry)
urlpatterns = [
    re_path('', include(router.urls)),
    re_path(r'^login/?$',views.LoginTokenObtainPairView.as_view(),name="Login"),
    re_path(r'^biometricLogin/?$',views.BiometricLoginTokenObtainPairView.as_view(),name="BiometricLogin"),
    re_path(r'login/refresh/?$',jwt_views.TokenRefreshView.as_view(),name="Refresh Login"),
    re_path(r'initBiometricAuthentication/?$',views.InitBiometricAuthentication.as_view(),name="InitBiometricAuthentication"),
    re_path(r'getBiometricToken/?$',views.GenerateBiometricTokenView.as_view(),name="GetBiometricToken"),
    re_path(r'logout/?$',views.LogoutUserView.as_view(),name="Logout")
    #path('', include())
]
