"""
URL configuration for LibraryAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include

from django.views.generic import RedirectView

# this is the url mapper, responsible for url routing 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')), 
    # any url starting with '' will be mapped to a url starting with 'catalog' 
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
]

