"""aite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','weib.views.index'),

    url(r'^signin$','weib.views.signin'),
    url(r'^signout$','weib.views.signout'),
    url(r'^update$','weib.views.update'),
    url(r'^friends$','weib.views.friends'),
    url(r'^load$','weib.views.load'),
    url(r'^hint$','weib.views.hint'),
    url(r'^callback','weib.views.callback'),
    
    url(r'^upload','weib.views.uploadimg')
 
]
