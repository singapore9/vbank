"""vbank URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from custom_auth.urls import api_patterns as custom_auth_api
from clients.urls import api_patterns as client_actions_api
from currencies.urls import api_patterns as currencies_api


api_patterns = [] + \
               custom_auth_api + \
               client_actions_api + \
               currencies_api

urlpatterns = [
    url(r'^api/', include(api_patterns)),
    url(r'^auth/', include('custom_auth.urls')),
    url(r'^admin/', admin.site.urls),
]
