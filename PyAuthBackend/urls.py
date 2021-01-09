"""PyAuthBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,re_path,include
from drf_yasg.views import get_schema_view
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="PyAuthBackend",
      default_version='v0.1',
      description="REST API to handle User Registration/Login.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="95adriano@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)
#login_required
urlpatterns = [
    re_path('^$', (schema_view.with_ui('swagger', cache_timeout=0))),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include('PyAuthBackend.AuthRESTAPI.urls')),
]
