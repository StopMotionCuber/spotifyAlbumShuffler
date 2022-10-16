"""spotifyAlbumShuffler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.views.generic import TemplateView
from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view

from .spotify import views
from .spotify.views import SpotifyPlaylistViewSet

router = routers.SimpleRouter()
router.register('playlists', SpotifyPlaylistViewSet)

urlpatterns = [
    path('album/', views.album_render),
    path('shuffle/', views.album_shuffle),
    path('login/', views.login),
    path('callback/', views.authorize),
    path('api/status/', views.status),
    path('api/', include(router.urls)),
    path('api/refresh/', views.refresh_playlists),
    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]
