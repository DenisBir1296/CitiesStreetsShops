"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from . import views
from . import models

router = routers.SimpleRouter()
router.register(r'city', views.CityViewSet)
router.register(r'shop', views.ShopViewSet)


urlpatterns = [
    path('data/', csrf_exempt(views.data)),
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
