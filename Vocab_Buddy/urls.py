"""
URL configuration for Vocab_Buddy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from learning import views as learning_views
from . import pwa

urlpatterns = [
    path('', learning_views.home, name='home'),
    path('manifest.webmanifest', pwa.manifest, name='manifest'),
    path('service-worker.js', pwa.service_worker, name='service_worker'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('words/', include('words.urls')),
    path('learning/', include('learning.urls')),
]
