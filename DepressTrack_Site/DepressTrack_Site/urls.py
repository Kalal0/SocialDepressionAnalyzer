"""DepressTrack_Site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from DepressTrack_App.views import home, result,Text_based, Twitter,Plotly


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('Text_based/', Text_based, name='Text_based'),
    path('Twitter/', Twitter, name='Twitter'),
    path('Twitter/Plotly/', Plotly, name='Plotly'),
    path('Text_based/result/', result, name='result')
]


urlpatterns += staticfiles_urlpatterns()